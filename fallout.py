import math
import requests
import json
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry


det_index = 0

windsock_marker = None
fallout_contours = []
fallout_points = {}
fallout_points[det_index] = []

fallout_drag_listener = None
marker_drag_listener = None
fallout_debug = False

fallout_current = None

# useful constants
deg2rad = (math.pi / 180)
rad2deg = (180 / math.pi)
ft2mi = 0.000189394
mi2km = 1.60934

sqmi2sqkm = 2.58999
sqkm2sqmi = 0.386102

# defaults
rad_doses = [1, 10, 100, 1000]
fallout_angle_default = 225

# used for color mixing
background_color = "e0e0e0"




class Fallout:
    def __init__(self):
        if fallout_debug:
            print("fallout object loaded")



    def lerp(self, x1, y1, x2, y2, y3):
        return ((y2 - y3) * x1 + (y3 - y1) * x2) / (y2 - y1)

    def log_lerp(self, x1, y1, x2, y2, y3):
        return self.lerp(x1, math.log(y1), x2, math.log(y2), math.log(y3))

    def get_wind_data(self, latitude, longitude):
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        # Make sure all required weather variables are listed here
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "hourly": ["wind_speed_10m", "wind_direction_10m"]
        }
        responses = openmeteo.weather_api(url, params=params)

        # Process first location
        response = responses[0]

        # Process hourly data
        hourly = response.Hourly()
        hourly_wind_speed_10m = hourly.Variables(0).ValuesAsNumpy()
        hourly_wind_direction_10m = hourly.Variables(1).ValuesAsNumpy()

        # Take the first wind speed and wind direction from the lists
        top_windspeed = hourly_wind_speed_10m[0]
        top_winddirection = hourly_wind_direction_10m[0]

        return top_windspeed, top_winddirection








    def SFSS_fallout_params(self, kt):
        if (kt < 1 or kt > 10 * math.pow(10, 5)) and not allowhuge:
            return False

        logW = math.log10(kt)  # to avoid recalculation

        # alpha values (p.249-250)
        alpha_2_3 = math.pow(10, -0.509 + 0.076 * logW)
        alpha_4 = math.pow(10, 0.270 + 0.089 * logW)
        alpha_5 = math.pow(10, -0.176 + 0.022 * logW)
        alpha_5pr = math.pow(10, -0.054 + 0.095 * logW)
        alpha_6 = math.pow(10, 0.030 + 0.036 * logW)
        alpha_7 = math.pow(10, 0.043 + 0.141 * logW)
        alpha_8 = math.pow(10, 0.185 + 0.151 * logW)
        if kt <= 28:
            alpha_9 = math.pow(10, 1.371 - 0.124 * logW)
        else:
            alpha_9 = math.pow(10, 0.980 + 0.146 * logW)

        # pre_reqs for X-distances (p.250)
        a_s = math.pow(10, 2.880 + 0.348 * logW)
        a = math.pow(10, 3.389 + 0.431 * logW)
        b = 1.40 * math.pow(10, 3) * math.pow(kt, 0.431)
        if kt <= 28:
            h = math.pow(10, 3.820 + 0.445 * logW)
        else:
            h = math.pow(10, 4.226 + 0.164 * logW)
        a_R_s = math.pow(10, 1.070 + 0.098 * logW)
        R_s = math.pow(10, 2.319 + 0.333 * logW)
        a_o = math.pow(10, math.log10(a) - (h * math.log10(a_R_s)) / (h - R_s))

        k_a = 2.303 * (math.log10(a_R_s) / (h - R_s))
        z_s = (2.303 * (math.log10(a_s) - math.log10(a_o))) / k_a  # typo in the original!!

        if kt >= 9:
            z_o = (1900 + (alpha_2_3 + 0.020) * z_s) / alpha_2_3
        else:
            z_o = (h - b)

        # X-distances (p.251)
        if kt <= 28:
            X_1 = -math.pow(10, 3.308 + 0.496 * logW)
            X_5 = math.pow(10, 3.644 + 0.467 * logW)
            X_6 = math.pow(10, 3.850 + 0.481 * logW)
            X_7 = math.pow(10, 3.862 + 0.586 * logW)
            X_8 = math.pow(10, 4.005 + 0.596 * logW)
            X_9 = math.pow(10, 5.190 + 0.319 * logW)
        else:
            X_1 = -math.pow(10, 3.564 + 0.319 * logW)
            X_5 = math.pow(10, 4.049 + 0.186 * logW)
            X_6 = math.pow(10, 4.255 + 0.200 * logW)
            X_7 = math.pow(10, 4.268 + 0.305 * logW)
            X_8 = math.pow(10, 4.410 + 0.315 * logW)
            X_9 = math.pow(10, 5.202 + 0.311 * logW)
        Y_s = math.pow(10, 3.233 + 0.400 * logW)

        # p. 250
        X_2 = alpha_2_3 * z_s - a_s
        X_3 = alpha_2_3 * z_s + a_s
        X_4 = (alpha_4 * (alpha_4 * z_o - 1900)) / (alpha_4 + 0.020)

        # intensity ridges (p.251)
        if kt <= 28:
            k_1_2 = math.pow(10, -2.503 - 0.404 * logW)
        else:
            k_1_2 = math.pow(10, -2.600 - 0.337 * logW)
        I_2_3 = math.pow(10, k_1_2 * (X_2 - X_1) / 2.303)

        if kt <= 28:
            a_h = math.pow(10, -0.431 - 0.014 * logW)
        else:
            a_h = math.pow(10, -0.837 + 0.267 * logW)
        a_b_2 = math.pow(10, 0.486 + 0.262 * logW)

        phi_5 = ((alpha_5 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_5 + a_h, 2))) / (
                    (alpha_5 - a_h) + math.sqrt(a_b_2 + math.pow(alpha_5 - a_h, 2)))
        phi_6 = ((alpha_6 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_6 + a_h, 2))) / (
                    (alpha_6 - a_h) + math.sqrt(a_b_2 + math.pow(alpha_6 - a_h, 2)))
        phi_7 = ((alpha_7 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_7 + a_h, 2))) / (
                    (alpha_7 - a_h) + math.sqrt(a_b_2 + math.pow(alpha_7 - a_h, 2)))
        phi_8 = ((alpha_8 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_8 + a_h, 2))) / (
                    (alpha_8 - a_h) + math.sqrt(a_b_2 + math.pow(alpha_8 - a_h, 2)))
        phi_9 = ((alpha_9 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_9 + a_h, 2))) / (
                    (alpha_9 - a_h) + math.sqrt(a_b_2 + math.pow(alpha_9 - a_h, 2)))
        phi_5pr = ((alpha_5 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_5 + a_h, 2))) / (alpha_2_3 + math.sqrt(a_b_2 + math.pow(alpha_2_3, 2)))
        phi_6pr = ((alpha_6 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_6 + a_h, 2))) / (alpha_2_3 + math.sqrt(a_b_2 + math.pow(alpha_2_3, 2)))
        phi_7pr = ((alpha_7 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_7 + a_h, 2))) / (alpha_2_3 + math.sqrt(a_b_2 + math.pow(alpha_2_3, 2)))
        phi_8pr = ((alpha_8 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_8 + a_h, 2))) / (alpha_2_3 + math.sqrt(a_b_2 + math.pow(alpha_2_3, 2)))
        phi_9pr = ((alpha_9 + a_h) + math.sqrt(a_b_2 + math.pow(alpha_9 + a_h, 2))) / (alpha_2_3 + math.sqrt(a_b_2 + math.pow(alpha_2_3, 2)))

        if kt <= 28:
            K_5_A_alpha = math.pow(10, -3.286 - 0.298 * logW)
        else:
            K_5_A_alpha = math.pow(10, -2.889 - 0.572 * logW)
        K_6_A_alpha = math.pow(10, -1.134 - 0.074 * logW)
        K_7_A_alpha = math.pow(10, -0.989 - 0.037 * logW)
        K_9_A_alpha = math.pow(10, -2.166 - 0.552 * logW)

        K_5pr_A_alpha = math.pow(10, -3.185 - 0.406 * logW)
        K_6pr_A_alpha = math.pow(10, -1.225 - 0.022 * logW)
        K_7pr_A_alpha = math.pow(10, -1.079 - 0.020 * logW)
        K_9pr_A_alpha = math.pow(10, -2.166 - 0.552 * logW)

        I_1 = 1  # set at 1 r/hr
        I_4 = 1  # set at 1 r/hr
        if alpha_5 >= a_h:
            I_5 = 4.606 * a * K_5_A_alpha * math.log10(phi_5)
        else:
            I_5 = 4.606 * a * K_5pr_A_alpha * math.log10(phi_5pr)
        if alpha_6 >= a_h:
            I_6 = 4.606 * a * K_6_A_alpha * math.log10(phi_6)
        else:
            I_6 = 4.606 * a * K_6pr_A_alpha * math.log10(phi_6pr)
        if alpha_7 >= a_h:
            I_7 = 4.606 * a * K_7_A_alpha * math.log10(phi_7)
        else:
            I_7 = 4.606 * a * K_7pr_A_alpha * math.log10(phi_7pr)
        # there is no I_8
        if alpha_9 >= a_h:
            I_9 = 4.606 * a * K_9_A_alpha * math.log10(phi_9)
        else:
            I_9 = 4.606 * a * K_9pr_A_alpha * math.log10(phi_9pr)

        # Y_8 is from a table with interpolation for other values
        # Each index here is a log10 of a yield (0 = 1KT, 1 = 10KT, 2 = 100KT, etc.)
        Y_8_vals = [6620, 12200, 48200, 167000, 342000, 650000]
        if (logW == round(logW) or kt == 1000) and (kt >= 1 and kt <= 100000):  # the log10 function botches
            Y_8 = Y_8_vals[round(logW)]
        else:
            if kt < 1:  # dubious interpolation
                Y_8 = 6620 / ((logW - math.log10(6620)) * -2)
            elif kt <= 100000:
                Y_8_1 = Y_8_vals[math.floor(logW)]
                Y_8_2 = Y_8_vals[math.ceil(logW)]
                Y_8 = Y_8_1 + (Y_8_2 - Y_8_1) * (math.pow(10, logW) / math.pow(10, math.ceil(logW)))
            elif kt > 100000:  # dubious interpolation
                Y_8 = 650000 * ((logW - math.log10(650000)) * 2)
        # alternative method that just curve fits
        # var Y_8 = Math.exp(((((9.968481E-4)*Math.log(kt)-.027025999)*Math.log(kt)+.22433052)*Math.log(kt)-.12350012)*Math.log(kt)+8.7992249);

        result = {
                'x1': X_1,
                'x2': X_2,
                'x3': X_3,
                'x4': X_4,
                'x5': X_5,
                'x6': X_6,
                'x7': X_7,
                'x8': X_8,
                'x9': X_9,
                'ys': Y_s,
                'y8': Y_8,
                'i1': I_1,
                'i2': I_2_3,
                'i3': I_2_3,
                'i4': I_4,
                'i5': I_5,
                'i6': I_6,
                'i7': I_7,
                'i9': I_9,
                'zo': z_o,
                'draw_stem': True  # or False, depending on your logic
            }

        return result  
            # returns in miles -- one might wonder why we separate this from the points function. It is so you can access this data (say, for the legend) without complete recalculation of all of the information.

        # rad_doses is an array of radiation doses in rads/hr to computer

        # fission fraction is a number less than or equal to 1 (100%) and greater than zero

    def SFSS_fallout(self, kt, rad_doses, fission_fraction, windspeed):
            x_var = 0
            y_var = 1
            i_var = 2
            p = self.SFSS_fallout_params(kt)

            if not fission_fraction:
                fission_fraction = 1

            if fallout_debug:
                print(p)

            dose_data = []

            for i in range(len(rad_doses)):
                rad = rad_doses[i] * (1 / fission_fraction)  # fission fraction decreases the overall radiation linearly.

                # create the dose_data object -- all input distances in feet, all output in miles
                d = {
                    'r': rad_doses[i],
                    'r_': rad,
                    'ff': fission_fraction,
                    'draw_stem': True if rad <= p['i2'] else False,  # quick test to see if we are above the stem threshold anyway
                    'draw_cloud': True if rad <= p['i7'] else False  # ditto
                }

                # draw_cloud:
                # rad <= p.i7 ? true : false  # ditto for cloud -- numbers above these values produce nonsense results
                draw_cloud = True if rad <= p['i7'] else False

                # max_cloud_rad:
                # p.i7 / (1 / fission_fraction)  # this allows us to report what the maximum mappable radiation level is for this yield -- note we take into account fission fraction here
                max_cloud_rad = p['i7'] / (1 / fission_fraction)

                # max_stem_rad:
                # p.i2 / (1 / fission_fraction)  # ditto
                max_stem_rad = p['i2'] / (1 / fission_fraction)

                # x_center: p.x2 * ft2mi
                x_center = p['x2'] * ft2mi

                # upwind_stem_distance: ((log_lerp(p.x1, p.i1, p.x2, p.i2, rad)) * ft2mi)
                upwind_stem_distance = self.log_lerp(p['x1'], p['i1'], p['x2'], p['i2'], rad) * ft2mi


                # downwind_stem_distance: ((log_lerp(p.x3, p.i3, p.x4, p.i4, rad)) * ft2mi)
                downwind_stem_distance = self.log_lerp(p['x3'], p['i3'], p['x4'], p['i4'], rad) * ft2mi

                # max_stem_width: ((log_lerp(0, p.i2, p.ys, 1, rad)) * ft2mi)
                max_stem_width = self.log_lerp(0, p['i2'], p['ys'], 1, rad) * ft2mi

                # upwind_cloud_distance: ((rad > p.i6 ? log_lerp(p.x6, p.i6, p.x7, p.i7, rad) : log_lerp(p.x5, p.i5, p.x6, p.i6, rad)) * ft2mi)
                upwind_cloud_distance = (self.log_lerp(p['x6'], p['i6'], p['x7'], p['i7'], rad) if rad > p['i6'] else self.log_lerp(p['x5'], p['i5'], p['x6'], p['i6'], rad)) * ft2mi

                # downwind_cloud_distance: ((log_lerp(p.x7, p.i7, p.x9, p.i9, rad)) * ft2mi)
                downwind_cloud_distance = self.log_lerp(p['x7'], p['i7'], p['x9'], p['i9'], rad) * ft2mi

                # max_cloud_width: (((p.y8 * log10(p.i7 / rad)) / (log10(p.i7 / p.i9))) * ft2mi)
                max_cloud_width = ((p['y8'] * math.log10(p['i7'] / rad)) / (math.log10(p['i7'] / p['i9']))) * ft2mi

                # cloud_widen_point: ((p.x7 + (p.x8 - p.x7) * (((p.y8 * log10(p.i7 / rad)) / (log10(p.i7 / p.i9))) / p.y8)) * ft2mi)
                cloud_widen_point = (p['x7'] + (p['x8'] - p['x7']) * (((p['y8'] * math.log10(p['i7'] / rad)) / (math.log10(p['i7'] / p['i9']))) / p['y8'])) * ft2mi

                # adjust for wind speed, uses Glasstone 1977's relation to change downwind values
                if windspeed > 15:
                    wm = 1 + ((windspeed - 15) / 60)
                elif windspeed < 15:
                    wm = 1 + ((windspeed - 15) / 30)
                if wm:
                    downwind_cloud_distance *= wm
                    downwind_stem_distance *= wm

                # estimate of the area enclosed -- sq mi
                if d['draw_stem']:
                    stem_area = (math.pi * ((downwind_stem_distance - upwind_stem_distance) / 2) * (x_center - upwind_stem_distance))
                else:
                    stem_area = 0
                if d['draw_cloud']:
                    cloud_area = (
                        # cloud ellipse 1
                        (math.pi * downwind_cloud_distance * max_cloud_width) / 2

                        # cloud ellipse 2
                        +
                        (math.pi * downwind_cloud_distance - ((cloud_widen_point) / 2 - (upwind_cloud_distance) / 2) * max_cloud_width) / 2
                    )
                else:
                    cloud_area = 0
                    
                dose_data = {}
                for i in range(len(rad_doses)):
                   rad = rad_doses[i] * (1 / fission_fraction)
                   draw_cloud = True if rad <= p['i7'] else False
                   draw_stem = True if rad <= p['i2'] else False
                   # calculate other parameters here...
                   dose_data[rad_doses[i]] = {
                       'draw_cloud': draw_cloud,
                       'max_cloud_rad': max_cloud_rad,
                       'max_stem_rad': max_stem_rad,
                       'x_center': x_center,
                       'upwind_stem_distance': upwind_stem_distance,
                       'downwind_stem_distance': downwind_stem_distance,
                       'max_stem_width': max_stem_width,
                       'upwind_cloud_distance': upwind_cloud_distance,
                       'downwind_cloud_distance': downwind_cloud_distance,
                       'max_cloud_width': max_cloud_width,
                       'cloud_widen_point': cloud_widen_point,
                       'stem_area': stem_area,
                       'cloud_area': cloud_area
                   }





                   

                if fallout_debug:
                   print(dose_data)
                return dose_data






               # f is a single dose_data object returned by the above function
    def SFSS_fallout_points(self, f, angle, steps):
                    p = []

                    if fallout_debug:
                        print(f)

                    stem_circle_radius = (f['x_center'] - f['upwind_stem_distance'])
                    stem_inner_x = math.sin(80 * deg2rad) * stem_circle_radius

                    if f['draw_stem']:


                        # stem top
                        draw_arc(p, f['upwind_stem_distance'], 0, f['x_center'], stem_circle_radius, steps / 2)
                        draw_arc(p, f['x_center'], stem_circle_radius, stem_inner_x, f['max_stem_width'], steps / 2)

                        # test if the stem and the cloud join
                        if ((f['upwind_cloud_distance'] + f['x_center']) < f['downwind_stem_distance']) and f['draw_cloud']:
                            pp = []
                            draw_arc(pp, f['upwind_cloud_distance'] + f['x_center'], 0, f['cloud_widen_point'] + f['x_center'], f['max_cloud_width'], steps)
                            pp = trim_points(pp, 1, f['max_stem_width'], "<")
                            add_points(p, pp)
                        else:
                            p.append([f['downwind_stem_distance'] * .8, f['max_stem_width']])
                            p.append([f['downwind_stem_distance'], 0])
                            if f['draw_cloud']:
                                draw_arc(p, f['upwind_cloud_distance'] + f['x_center'], 0, f['cloud_widen_point'] + f['x_center'], f['max_cloud_width'], steps)
                    else:
                        if f['draw_cloud']:
                            draw_arc(p, f['upwind_cloud_distance'] + f['x_center'], 0, f['cloud_widen_point'] + f['x_center'], f['max_cloud_width'], steps)

                    if f['draw_cloud']:
                        # cloud
                        draw_arc(p, f['cloud_widen_point'] + f['x_center'], f['max_cloud_width'], f['downwind_cloud_distance'] - f['x_center'] * 2, 0, steps)
                        draw_arc(p, f['downwind_cloud_distance'] - f['x_center'] * 2, 0, f['cloud_widen_point'] + f['x_center'], -f['max_cloud_width'], steps)
                    if f['draw_stem']:
                        # stem bottom
                        if ((f['upwind_cloud_distance'] + f['x_center']) < f['downwind_stem_distance']) and f['draw_cloud']:
                            pp = []
                            draw_arc(pp, f['cloud_widen_point'] + f['x_center'], -f['max_cloud_width'], f['upwind_cloud_distance'] + f['x_center'], 0, steps)
                            pp = trim_points(pp, 1, -f['max_stem_width'], ">")
                            add_points(p, pp)
                        else:
                            if f['draw_cloud']:
                                draw_arc(p, f['cloud_widen_point'] + f['x_center'], -f['max_cloud_width'], f['upwind_cloud_distance'] + f['x_center'], 0, steps)
                            p.append([f['downwind_stem_distance'], 0])
                            p.append([f['downwind_stem_distance'] * .8, -f['max_stem_width']])
                        draw_arc(p, stem_inner_x, -f['max_stem_width'], f['x_center'], -stem_circle_radius, steps / 2)
                        draw_arc(p, f['x_center'], -stem_circle_radius, f['upwind_stem_distance'], 0, steps / 2)
                    else:
                        if f['draw_cloud']:
                            draw_arc(p, f['cloud_widen_point'] + f['x_center'], -f['max_cloud_width'], f['upwind_cloud_distance'] + f['x_center'], 0, steps)

                    p = rotate_points(p, angle)

                    return p






    



    # main fallout function
    def do_fallout(kt, fission_fraction, fallout_info_div_id, airburst, hob_ft):
        if fallout_debug:
            print("do_fallout")
        if DEBUG:
            print("do_fallout")

        if ((kt < 1) or (kt > 10 * pow(10, 5))) and not allowhuge:
            if fallout_info_div_id is not None:
                print("dawg only between 1-100")
            return False

        # Use the wind speed and direction from the API
        angle = wind_direction
        wind = wind_speed

        if not angle:
            angle = 0

        if hob_ft:
            kt_frac = fallout_kt_hob(kt, fission_fraction, hob_ft)
        else:
            kt_frac = 0

        fallout_current = {
            'kt': kt,
            'wind': wind_speed,
            'fission_fraction': fission_fraction,
            'fallout_info_div_id': fallout_info_div_id,
            'rad_doses': rad_doses,
            'angle': angle,
            'airburst': airburst,
            'hob_ft': hob_ft,
            'kt_frac': kt_frac,
        }

       # draw_fallout()






if fallout_debug:
    print(sfss)

steps = 15

det_index = 0


if fallout_current is None or 'rad_doses' not in fallout_current:
    print("Error: fallout_current is None or does not contain 'rad_doses'")
else:
    fallout_points[det_index] = []
    for i in range(len(fallout_current['rad_doses'])):
        if 'angle' in fallout_current and fallout_current['angle'] is not None:
            dets[det_index]['fallout_angle'] = round(fallout_current['angle'])
        else:
            print("Error: fallout_current['angle'] is None")

        if 'rad_doses' in fallout_current and fallout_current['rad_doses'] is not None:
            dets[det_index]['fallout_rad_doses'] = fallout_current['rad_doses']
        else:
            print("Error: fallout_current['rad_doses'] is None")

    # render the points at 0 angle first -- for whatever reason that seems to need to be -90
    points = fo.SFSS_fallout_points(ss, -90, steps)
    # save them
    fallout_points[det_index].append(points)
    # then rotate them
    plot_fallout(pos, rotate_points(points, fallout_current['angle']), f_color, str(fallout_current['rad_doses'][i]) + " r/hr")
               
            # this scales the fission yield according to height of burst. Input is kt, fission_fraction (0-1), height of burst (feet)
            # returns a new kilotonnage, or 0 if the hob is too high for local fallout
            # taken from eq. 4.4.1 of H.G. Norment, "DELFIC: Department of Defense Fallout Prediction System, Vol. I-Fundamentals" (DNA 5159F-1, 31 December 1979), page 53. 
    def fallout_kt_hob(kt, fission_fraction, hob):
        if hob == 0:
            return kt  # surface burst, no doubt
        fission_kt = kt * (fission_fraction / 100)
        scaled_hob_activity_decay_constant = hob / pow(kt, (1 / 3))
        scaled_hob = hob / pow(kt, (1 / 3.4))
        max_hob = 180 * pow(kt, .4)  # Glasstone and Dolan, 1977 edn., p.71
        if hob >= max_hob:  # using Glasstone' def of negligible fallout rather than DELFICs, because DELFICs seems about 40-50% lower for no reason
            return 0
        elif scaled_hob_activity_decay_constant <= 0:
            return 0
        else:
            f_d = pow(0.45345, scaled_hob_activity_decay_constant / 65)
            scaled_kt = (fission_kt * f_d) / (fission_fraction / 100)
            return scaled_kt

    # Use the wind direction from the API
    new_angle = wind_direction
    if new_angle < 0:
        new_angle += 360

    # Redraw the fallout if the angle has changed
    if fallout_current.angle != new_angle:
        fallout_current.angle = new_angle
       # redraw_fallout()


                

            # changes which doses are displayed
    def change_doses():
                current = ''
                for i in range(len(rad_doses)):
                    current += str(rad_doses[i])
                    if i < len(rad_doses) - 1:
                        current += ","
                input_doses = window.prompt("To change the doses plotted in the fallout curves, enter them in below as numbers separated by commas. These numbers are in rads/hour, between 1 and 30,000. Invalid numbers will be ignored.", current)

                if input_doses:
                    new_doses = []
                    input_doses_array = input_doses.split(",")
                    for i in range(len(input_doses_array)):
                        n = int(input_doses_array[i])
                        if ((n > 0) and (n <= 30000)) or allowhuge:
                            new_doses.append(n)
                    if len(new_doses) > 0:
                        rad_doses = new_doses
                        rad_doses.sort()
                        if fallout_current:
                            fallout_current.rad_doses = rad_doses
                           # draw_fallout()
                dets[det_index].rad_doses = fallout_current.rad_doses
                update_permalink()

            # rotates an array of points to a certain angle
            # note that this now returns a new array. previously it was
            # modifying the underlying points_array which was creating problems.
    def rotate_points(points_array, angle_degrees):
                rotated = []
                # normalize angle for wind
                angle_degrees = (90 - angle_degrees) + 180
                # rotate
                angle_rad = (angle_degrees) * deg2rad
                sinA = math.sin(angle_rad)
                cosA = math.cos(angle_rad)
                for i in range(len(points_array)):
                    px = points_array[i][0]
                    py = points_array[i][1]
                    rotated.append([px * cosA - py * sinA, px * sinA + py * cosA])
                return rotated

    # clears fallout contours
    def clear_fallout():
        if DEBUG:
            print("clear_fallout")
        if fallout_contours[det_index]:
            if len(fallout_contours[det_index]) > 0:
                for i in range(len(fallout_contours[det_index])):
                    fallout_contours[det_index][i].remove()
                fallout_contours[det_index] = None


    # determine fallout exposure at a point
    # returns in rad/hr at H+1
    def h1_dose_at_point(sample_lat, sample_lon, gz_lat, gz_lon):
        if not fallout_current:
            print("No fallout object")
            return False

        dist = distance_between(gz_lat, gz_lon, sample_lat, sample_lon) * km2mi
        abs_bearing = get_bearing(gz_lat, gz_lon, sample_lat, sample_lon)
        rel_bearing = abs(normalize_bearing(fallout_current['angle'] - 180) - abs_bearing)
        dw_dist = (math.cos(rel_bearing * deg2rad) * dist) * km2mi  # downwind distance along centerline (x axis) -- note negative is upwind
        cw_dist = abs(math.sin(rel_bearing * deg2rad) * dist) * km2mi  # crosswind distance perpendicular to centerline (y axis) -- note this is absolute

        # first get 1 rad info
        steps = 15

        if fallout_current['kt_frac'] and fallout_current['airburst']:
            sfss = fo.SFSS_fallout(fallout_current['kt_frac'], [1], (fallout_current['fission_fraction'] / 100), fallout_current['wind'])
        else:
            sfss = fo.SFSS_fallout(fallout_current['kt'], [1], (fallout_current['fission_fraction'] / 100), fallout_current['wind'])

        # quick check for 1 rad
        if not point_in_poly([sample_lat, sample_lon], points_to_ll(gz_lat, gz_lon, fo.SFSS_fallout_points(sfss[1], fallout_current['angle'], steps))):
            rad_hr = 0
        else:
            # use this to also get max rad
            max_rad = max(sfss[1]['max_cloud_rad'], sfss[1]['max_stem_rad'])
            if max_rad > 30000 and not allowhuge:
                max_rad = 30000
            max_rad = round(max_rad)
            # first check the max
            if is_inside_contour(max_rad, sample_lat, sample_lon, gz_lat, gz_lon, steps):
                rad_hr = max_rad
            else:
                rad_hr = search_between_contours(1, max_rad, sample_lat, sample_lon, gz_lat, gz_lon, steps)
        return rad_hr


    # this is sort of a simple binary search -- seems to work, usually no more than 13 steps, gets same results as brute force
    def search_between_contours(low, high, sample_lat, sample_lon, gz_lat, gz_lon, steps):
        half = round((high + low) / 2)
        if high <= low or half <= low or high == low + 1:
            return low
        s1 = is_inside_contour(low, sample_lat, sample_lon, gz_lat, gz_lon, steps)
        s2 = is_inside_contour(half, sample_lat, sample_lon, gz_lat, gz_lon, steps)
        if s1 and not s2:
            return search_between_contours(low, half, sample_lat, sample_lon, gz_lat, gz_lon, steps)
        if not s1 and s2:
            return search_between_contours(half, high, sample_lat, sample_lon, gz_lat, gz_lon, steps)
        if s1 and s2:
            return search_between_contours(half, high, sample_lat, sample_lon, gz_lat, gz_lon, steps)

        return False  # something went wrong


    # for a given sample_lat and sample_lon, will work out if it is inside a given fallout contour
    def is_inside_contour(rad, sample_lat, sample_lon, gz_lat, gz_lon, steps):
        if fallout_current['kt_frac'] and fallout_current['airburst']:
            sfss = fo.SFSS_fallout(fallout_current['kt_frac'], [rad], (fallout_current['fission_fraction'] / 100), fallout_current['wind'])
        else:
            sfss = fo.SFSS_fallout(fallout_current['kt'], [rad], (fallout_current['fission_fraction'] / 100), fallout_current['wind'])
        if not point_in_poly([sample_lat, sample_lon], points_to_ll(gz_lat, gz_lon, fo.SFSS_fallout_points(sfss[rad], fallout_current['angle'], steps))):
            return 0
        else:
            return 1


    # converts a series of points (which are distances from some central point in km)
    # into latitude and longitude pairs based on their distances from the actual
    # lat/lon of the central point
    def points_to_ll(gzlat, gzlng, points):
        R = 6371  # Earth's mean radius in km
        coords = []
        for i in range(len(points)):
            lat = gzlat + rad2deg * (points[i][1] * mi2km / R)
            lng = gzlng + rad2deg * (points[i][0] * mi2km / R / math.cos(deg2rad * gzlat))
            coords.append([lat, lng])
        return coords

    # determines whether a point is in a given polygon
    def point_in_poly(point, vs):
        x = point[0]
        y = point[1]

        inside = False
        for i in range(len(vs)):
            j = len(vs) - 1 if i == 0 else i - 1
            xi, yi = vs[i]
            xj, yj = vs[j]

            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside
        return inside

    # creates an array of distances of a list of coordinates ([lat,lon]) from a central lat/lon
    def distances(lat, lon, coords):
        dists = []
        for coord in coords:
            dists.append(distance_between(lat, lon, coord[0], coord[1]))
        dists.sort()
        return dists


    # same as Math.pow, just cleans up the function a bit
    def pow(n, x):
        return math.pow(n, x)

    def log(n):
        return math.log(n)

    def log10(n):
        return math.log(n) / math.log(10)

    def unlog10(n):
        return pow(10, n)

fo = Fallout()




wind_speed, wind_direction = fo.get_wind_data(52.52, 13.41)



# Prompt the user for the necessary parameters
kt = float(input("Enter the yield of the explosion in kilotons: "))
fission_fraction = float(input("Enter the fraction of the yield that is due to fission (0-1): "))
hob = float(input("Enter the height of the burst in feet: "))

# Define the radiation doses for which we want to calculate the fallout contours
rad_doses = [1, 10, 100, 1000]

# Calculate the fallout parameters for each radiation dose
for rad in rad_doses:
    sfss = fo.SFSS_fallout(kt, [rad], fission_fraction, wind_speed)
    params = sfss[rad]
    if 'draw_stem' in params and params['draw_stem']:
        # Print the fallout contour information
        print(f"Fallout contour for {rad} rads per hr:")
        print(f"Maximum downwind fallout (stem only) distance: {params['downwind_stem_distance']*1.60934} km")
        print(f"Maximum stem width: {params['max_stem_width']*1.60934} km")
        print(f"Approximate area affected: {params['stem_area']*2.58999} km²")
    if params['draw_cloud']:
        print(f"Maximum downwind fallout distance: {params['downwind_cloud_distance']*1.60934} km")
        print(f"Maximum width: {params['max_cloud_width']*1.60934} km")
        print(f"Approximate area affected: {(params['stem_area'] + params['cloud_area'])*2.58999} km²")




'''


                    # draws a partial arc joining points x1, y1 and x2, y2 centered at xc, yc
    def draw_arc(p, x1, y1, x2, y2, steps):
                        if x1 < x2:
                            if y1 < y2:
                                # top left
                                xc = x2
                                yc = y1
                            else:
                                # top right
                                xc = x1
                                yc = y2
                        else:
                            if y1 < y2:
                                # bottom left
                                xc = x1
                                yc = y2
                            else:
                                # bottom right
                                xc = x2
                                yc = y1

                        e_width = abs(xc - x1 if xc == x1 else xc - x2)
                        e_height = abs(yc - y1 if yc == y1 else yc - y2)

                        start_angle = math.atan2(y1 - yc, x1 - xc)
                        stop_angle = math.atan2(y2 - yc, x2 - xc)

                        if start_angle < 0:
                            start_angle += math.pi * 2

                        step = (stop_angle - start_angle) / steps

                        if step < 0:
                            for theta in range(start_angle, stop_angle, step):
                                x = xc + e_width * math.cos(theta)
                                y = yc + e_height * math.sin(theta)
                                p.append([x, y])
                        else:
                            for theta in range(start_angle, stop_angle, step):
                                x = xc + e_width * math.cos(theta)
                                y = yc + e_height * math.sin(theta)
                                p.append([x, y])
                        p.append([x2, y2])


                    # trims points based on criteria
                    # input is an array of points (p), a lat/lng flag (0 = lat, 1 = lng), a value to compare to (compare), and a comparison mode (string)
    def trim_points(p, latlng, compare, mode):
                        pp = []
                        for i in range(len(p)):
                            bad = False
                            if mode == "<":
                                bad = p[i][latlng] < compare
                            elif mode == "<=":
                                bad = p[i][latlng] <= compare
                            elif mode == ">":
                                bad = p[i][latlng] > compare
                            elif mode == ">=":
                                bad = p[i][latlng] >= compare
                            elif mode == "==":
                                bad = p[i][latlng] == compare
                            elif mode == "!=":
                                bad = p[i][latlng] != compare
                            if not bad:
                                pp.append(p[i])
                        return pp


                    # adds points arrays from pp to p
    def add_points(p, pp):
                        for i in range(len(pp)):
                            p.append(pp[i])


                    # creates the fallout polygon from points and adds it to the map
    def plot_fallout(gz, points, color, legend):
                        R = 6371  # Earth's mean radius in km
                        coords = []
                        if color[0] != "#":
                            color = "#" + color

                        gzlat = latval(gz)
                        gzlng = lngval(gz)

                        coords = points_to_ll(gzlat, gzlng, points)
                        coords = [{'lat': p[0], 'lon': p[1]} for p in coords]

                        if not fallout_contours[det_index]:
                            fallout_contours[det_index] = []
                        if fallout_contours[det_index]:
                            zoff = len(fallout_contours[det_index]) + 1
                        else:
                            zoff = 1
                        poly = MAPUI.polygon({
                            'latLons': coords,
                            'stroke': False,
                            'fillColor': color,
                            'fillOpacity': 0.25,
                            'map': map,
                            'visible': True,
                            'underLayer': "falloutLayer",
                            'zindex': -10 * (-det_index + 1) + zoff,
                        })
                        fallout_contours[det_index].append(poly)

'''





























#above if fallout debug.

    # draws fallout using the current settings. we keep these separate from the other function so I can just call it whenever I want to refresh it.
    # it would be better to make a refresh fallout function that didn't recreate everything from scratch, just re-projected the coordinates.
    # is that possible? would need to store the original coordinate points.
   # def draw_fallout():
      #  if DEBUG:
       #     print("draw_fallout")
       # if fallout_debug:
       #     print('draw_fallout')
       # if fallout_current:
         #   if fallout_contours[det_index] is not None:
         #       clear_fallout()

        #    if fallout_current['airburst'] and fallout_current['kt_frac'] == 0:
            #    if len(fallout_info) > 0:
            #        o = ""
             #       o += "<hr>"
          #  #        o += "<p><b>Fallout:</b> Your choice of burst height is too high to produce significant local fallout. The minimum burst height to produce appreciable fallout for a yield of " + ktOrMt(fallout_current['kt']) + " is " + unit(180 * pow(fallout_current['kt'], .4) * ft2km, "km") + "."
    #                fallout_info = o
   #             if len(fallout_info) > 0:
                    # additional code here
    #                pass
  #      else:
   #         # Use the wind direction and speed from the API
    #        angle = wind_direction
     #       wind = wind_speed
#
 #           pos = marker.getLatLon()
  #          if fallout_current['kt_frac'] and fallout_current['airburst']:
   #             sfss = fo.SFSS_fallout(fallout_current['kt_frac'], fallout_current['rad_doses'], (fallout_current['fission_fraction'] / 100), fallout_current['wind'])
    #        else:
     #           sfss = fo.SFSS_fallout(fallout_current['kt'], fallout_current['rad_doses'], (fallout_current['fission_fraction'] / 100), fallout_current['wind'])
      #      if fallout_info:
               # o = ""
       #         o += "<hr><div>"
        #        o += "Estimated <b>fallout radiation intensity contours</b> for a " + ktOrMt(fallout_current['kt'])
         #       if fallout_current['airburst'] and fallout_current['kt_frac']:
          #          o += " airburst*"
           #     else:
            #        o += " surface burst"
             #   if fallout_current['fission_fraction'] < 100:
              #      o += " (" + (round(fallout_current['fission_fraction']) if fallout_current['fission_fraction'] > 1 else fallout_current['fission_fraction']) + "% fission)"
               # o += " with a " + unit(fallout_current['wind'], "mph", {'round_precision': 0}) + " wind at one hour after detonation: "
                #o += "<span class='hider-arrow expanded' expanded='1' div='effects_captions_fallout' onclick='expand_div(this);'> </span>"
               # o += "<div class='collapsed-content' id='effects_captions_fallout'>"
