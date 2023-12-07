from math import log
import math 


class NukeEffects:
    def __init__(self):
        self.ambient_pressure = 14.7
        self.error = None
        self.debug = False
        self.eq = {}
        self.eq['2-4'] = {'xmin': 0.0472, 'xmax': 4.82, 'args': [-0.1877932, -1.3986162, 0.3255743, -0.0267036]}
        self.eq['2-5'] = {'xmin': 0.1, 'xmax': 200, 'args': [-0.1307982, -0.6836211, 0.1091296, -0.0167348]}
        self.eq['2-19'] = {'xmin': 1, 'xmax': 200, 'args': [-0.0985896, -0.6788230, 0.0846268, -0.0089153]}
        self.eq['2-25'] = {'xmin': 1, 'xmax': 200, 'args': [-0.0564384, -0.7063068, 0.0838300, -0.0057337]}
        self.eq['2-31'] = {'xmin': 1, 'xmax': 100, 'args': [-0.0324052, -0.6430061, -0.0307184, 0.0375190]}
        self.eq['2-37'] = {'xmin': 1, 'xmax': 50, 'args': [-0.0083104, -0.6809590, 0.0443969, 0.0032291]}
        self.eq['2-43'] = {'xmin': 1, 'xmax': 50, 'args': [0.0158545, -0.7504681, 0.1812493, -0.0573264]}
        self.eq['2-49'] = {'xmin': 1, 'xmax': 30, 'args': [0.0382755, -0.8763984, -0.4701227, -0.02046373]}
        self.eq['2-55'] = {'xmin': 1, 'xmax': 20, 'args': [0.0468997, -0.7764501, 0.3312436, -0.1647522]}
        self.eq['2-61'] = {'xmin': 1, 'xmax': 200, 'args': [0.1292768, -0.7227471, 0.0147366, 0.0135239]}
        self.eq['2-60'] = {'xmin': 0.0508, 'xmax': 1.35, 'args': [0.1829156, -1.4114030, -0.0373825, -0.1635453]}
        self.eq['2-6'] = {'xmin': 0.0615, 'xmax': 4.73, 'args': [-1.9790344, -2.7267144, 0.5250615, -0.1160756]}
        self.eq['2-62'] = {'xmin': 0.154, 'xmax': 1.37, 'args': [1.2488468, -2.7368746]}
        self.eq['2-64'] = {'xmin': 0.0932, 'xmax': 0.154, 'args': [-3.8996912, -6.0108828]}
        self.eq['2-8'] = {'xmin': 0.0677, 'xmax': 0.740, 'args': [-0.1739890, 0.5265382, -0.0772505, 0.0654855]}
        self.eq['2-12'] = {'xmin': 0.0570, 'xmax': 1.10, 'args': [0.6078753, 1.1039021, -0.2836934, 0.1006855]}
        self.eq['2-16'] = {'xmin': 0.0589, 'xmax': 4.73, 'args': [1.3827823, -1.3518147, 0.1841482, 0.0361427]}
        self.eq['2-74'] = {'xmin': 0.2568, 'xmax': 1.4, 'args': [1.7110032, -1.2000278, 0.8182584, 1.0652528]}
        self.eq['2-76'] = {'xmin': 0.0762, 'xmax': 0.2568, 'args': [3.8320701, 5.6357427, 6.6091754, 1.5690375]}
        self.eq['2-78'] = {'xmin': 1, 'xmax': 200, 'args': [3.2015016, -0.3263444]}
        self.eq['2-79'] = {'xmin': 0.0512, 'xmax': 1.35, 'args': [3.1356018, 0.3833517, -0.1159125]}
        self.eq['2-106'] = {'xmin': 0.05, 'xmax': 50, 'args': [-0.0401874, -2.0823477, -0.0511744, -0.0074958]}
        self.eq['2-108'] = {'xmin': 0.0001, 'xmax': 100, 'args': [-0.0193419, -0.4804553, -0.0055685, 0.0002013]}
        self.eq['2-110'] = {'xmin': 1, 'xmax': 100000, 'args': [0.3141555, 0.059904, 0.0007636, -0.0002015]}
        self.eq['2-111'] = {'xmin': 1, 'xmax': 100000, 'args': [0.6025982, 0.0201394, 0.0139640, 0.0008559]}


        self.eq['77-12.65-1st-50'] = {'xmin': 1, 'xmax': 20000, 'args': [1.93566176470914,0.325315457507999,-0.113516274769641,0.0300971575115961,-0.00330445814836616,0.000129665656335876]}
        self.eq['77-12.65-2nd-50'] = {'xmin': 1, 'xmax': 20000, 'args': [4.0147058823566697E+00,3.7180525416799937E-01,-4.5026131075683193E-02,1.3549565337157871E-02,-1.6559848551158524E-03,7.0380159845451207E-05]}
        self.eq['77-12.65-3rd-50'] = {'xmin': 1, 'xmax': 20000, 'args': [5.9981617647112317E+00,5.3350791551060528E-01,-2.3435878115600033E-02,1.0395274013807305E-02,-1.4366360115630195E-03,6.3930657856814399E-05]}
        self.eq['77-12.65-noharm-100'] = {'xmin': 1, 'xmax': 20000, 'args': [1.14705882353066,0.124659908645308,-0.0160088216223604,0.00359441786929512,-0.000263841056172493,0.0000053050769836388]}
        self.eq['77-12.65-3rd-100'] = {'xmin': 1, 'xmax': 20000, 'args': [7.0018382352996857,.55437306382914320,.056501270479506649,-.015219252753643841,.0017062986685328282,-.000067950215125955893]}
        self.eq['2-115'] = {'xmin': 10, 'xmax': 20000, 'args': [-2.1343121,5.6948378,-5.7707609,2.7712520,-0.6206012,0.0526380]}


    
    hobs = {}  # heights
    rngs = {}  # corresponding ranges
    hobs[10000] = [0, 10, 22, 33, 44, 54, 65, 73, 79, 88, 94, 99, 104, 108, 111, 114, 116, 117, 117, 117]
    rngs[10000] = [69, 70, 70, 71, 71, 71, 70, 68, 66, 63, 58, 53, 47, 40, 33, 26, 18, 11, 3, 0]
    hobs[5000] =  [0,10,22,35,46,57,68,78,90,99,106,113,119,125,131,135,138,141,143,144,145,146]
    rngs[5000] =  [88,88,89,90,90,90,89,88,85,81,78,74,69,63,55,48,41,34,26,17,9,0]
    hobs[2000] =  [0,7,16,26,36,45,55,67,77,86,96,104,113,121,130,138,144,151,156,161,167,172,177,180,183,186,188,190,191,192]
    rngs[2000] =  [119,119,120,121,122,122,122,122,122,121,120,119,117,115,112,108,105,100,94,88,81,73,64,56,48,40,30,21,11,0]
    hobs[1000] =  [0,7,17,27,37,47,58,71,82,94,104,115,126,135,144,153,161,170,178,184,191,196,202,206,210,214,218,222,225,228,230,232,234,236,237,238,239]
    rngs[1000] =  [154,154,154,155,155,156,156,157,157,158,157,156,154,152,149,146,142,137,131,127,121,115,108,102,96,91,83,75,67,59,52,43,33,24,15,8,0]
    hobs[500] =  [0,9,19,29,39,50,61,76,89,103,118,130,142,153,166,179,191,199,209,221,229,236,244,250,256,261,266,271,277,281,284,286,289,290,291]
    rngs[500] =  [193,194,195,196,198,199,200,202,203,203,204,203,202,200,198,194,189,184,179,170,163,154,144,134,125,117,107,96,84,73,60,48,33,18,0]
    hobs[200] =  [0,13,26,39,54,69,86,103,119,136,156,177,195,209,227,240,249,258,266,274,283,290,302,310,317,324,331,338,343,349,356,362,367,372,376,380,382,386,387,390]
    rngs[200] =  [264,264,265,265,266,266,267,268,269,269,270,270,269,268,265,261,257,253,249,243,238,231,221,213,204,195,186,175,166,155,142,131,121,107,94,78,64,44,32,0]
    hobs[100] =  [0,10,25,42,60,78,96,113,131,152,175,194,212,230,249,269,286,299,313,326,338,349,360,368,377,386,394,400,407,415,422,429,438,447,455,462,468,474,478,485,489,493,496,498,500,501]
    rngs[100] =  [342,342,343,345,345,346,347,348,350,351,353,354,355,355,355,354,353,351,349,344,339,332,324,317,307,297,287,279,270,258,247,237,223,206,191,176,163,149,135,117,100,81,58,39,17,0]
    hobs[50] =  [0,19,50,90,136,174,209,244,279,319,346,371,391,406,427,447,459,472,481,490,504,516,527,537,548,558,568,579,588,598,606,613,620,625,630,633,635,637,638]
    rngs[50] =  [459,459,461,463,465,469,473,478,483,489,492,493,492,490,484,474,463,442,427,406,386,365,347,329,310,290,270,250,227,202,181,159,138,115,90,68,46,20,0]
    hobs[30] =  [0,24,54,84,114,143,179,215,250,292,328,365,403,441,476,502,527,552,574,587,589,591,596,612,628,647,665,685,703,721,736,747,758,766,773,779,782,784]
    rngs[30] =  [592,593,593,594,594,596,597,600,604,609,612,618,624,631,638,642,642,640,628,609,585,557,524,486,453,421,392,353,319,280,244,214,180,141,107,65,21,0]
    hobs[20] =  [0,34,84,130,176,223,274,319,358,399,427,458,485,512,537,566,597,627,651,673,687,694,692,683,674,672,672,677,685,697,713,730,748,764,781,801,814,827,844,858,870,881,892,898,906,912,919,922,924]
    rngs[20] =  [714,719,727,737,747,757,771,782,795,812,826,843,860,879,898,914,922,919,907,887,860,826,788,757,729,704,686,662,639,612,586,559,533,508,478,446,419,394,358,327,297,269,232,205,165,124,68,26,0]
    hobs[15] = [0,27,67,114,160,209,250,294,319,359,398,434,459,488,515,538,565,594,624,650,676,692,711,726,739,750,761,771,776,779,778,773,764,751,738,731,733,740,750,765,780,798,815,831,845,861,874,889,907,921,935,948,958,968,980,1000,1004,1017,1033,1041]
    rngs[15] =  [818,827,840,858,873,893,912,933,946,974,1002,1033,1057,1083,1111,1133,1158,1178,1193,1196,1191,1183,1173,1161,1146,1129,1109,1082,1058,1028,990,956,923,892,865,838,811,784,757,727,698,668,640,615,589,563,539,512,481,452,425,397,377,352,331,277,215,153,74,0]
    hobs[10] =  [0,30,73,115,151,191,235,269,312,345,380,412,442,471,500,528,558,592,627,658,692,724,749,767,785,805,820,835,851,862,872,881,888,893,896,894,888,881,872,859,850,846,848,852,858,867,880,891,904,916,926,941,953,965,980,989,1000,1017,1045,1074,1103,1136,1169,1190,1215,1236,1244,1252,1260]
    rngs[10] =  [1024,1037,1056,1074,1092,1112,1133,1151,1173,1193,1214,1238,1261,1285,1312,1336,1360,1387,1412,1430,1447,1455,1455,1450,1443,1433,1422,1407,1388,1370,1348,1320,1291,1265,1246,1227,1196,1173,1148,1119,1097,1065,1047,1026,1007,983,957,934,911,890,874,852,833,814,795,778,765,740,690,636,583,512,450,380,293,211,128,58,0]
    hobs[8] =  [0,83,161,256,364,459,587,661,744,847,930,975,996,1004,983,950,934,942,967,1029,1095,1145,1198,1244,1289,1314,1351,1384,1401,1417]
    rngs[8] =  [1124,1169,1223,1277,1347,1409,1492,1558,1636,1694,1694,1645,1591,1550,1483,1376,1289,1194,1103,1012,909,831,740,649,550,496,393,248,145,0]
    hobs[6] =  [0,62,120,202,273,364,434,500,595,686,777,888,979,1041,1083,1095,1079,1054,1025,1025,1033,1074,1145,1227,1310,1368,1421,1488,1537,1570,1570,1603,1628,1645,1653,1653]
    rngs[6] =  [1339,1393,1438,1500,1554,1624,1682,1740,1822,1893,1959,2012,2017,1988,1926,1843,1756,1669,1570,1508,1450,1360,1240,1132,1008,926,847,723,603,512,492,384,256,124,37,0]
    hobs[4] =  [0,37,87,153,244,331,421,529,661,777,905,988,1070,1132,1186,1231,1240,1223,1198,1182,1174,1194,1260,1326,1413,1521,1612,1694,1781,1860,1913,1971,2017,2050,2074,2087,2087]
    rngs[4] =  [1665,1702,1764,1847,1946,2045,2136,2244,2364,2459,2554,2599,2624,2620,2591,2512,2438,2331,2227,2153,2050,1942,1798,1686,1570,1426,1310,1182,1058,926,810,657,496,343,182,62,0]
    hobs[2] =  [0,25,58,136,186,227,293,368,434,479,529,591,632,686,740,798,851,921,1017,1099,1198,1264,1318,1372,1413,1430,1429,1421,1422,1438,1508,1587,1702,1818,1988,2190,2302,2426,2492,2517,2612,2698,2793,2893,2971,3041,3079,3103,3136,3157,3178,3190,3202,3211]
    rngs[2] =  [2558,2616,2682,2847,2942,3033,3136,3281,3380,3467,3545,3632,3702,3781,3868,3942,4021,4099,4182,4207,4182,4136,4079,3992,3901,3777,3649,3525,3401,3264,3116,3000,2876,2752,2579,2364,2236,2091,2000,1971,1839,1707,1537,1351,1161,950,793,682,545,442,302,182,70,0]
    hobs[1] = [0,58,140,219,322,405,496,579,678,810,888,971,1083,1165,1260,1388,1533,1665,1727,1802,1864,1888,1913,1921,1922,1938,2004,2140,2355,2512,2785,3012,3211,3335,3525,3702,3764,3909,4017,4157,4236,4318,4409,4463,4521,4632,4702,4781,4860,4897,4934,4963,4992,5012,5008,5070]
    rngs[1] = [3860,3996,4248,4475,4744,4996,5236,5471,5719,6037,6219,6397,6583,6715,6835,6946,7021,7021,6979,6872,6698,6512,6256,6021,5781,5558,5364,5149,4913,4756,4508,4293,4107,3975,3785,3591,3508,3343,3207,3008,2884,2756,2612,2500,2405,2157,2008,1764,1504,1335,1149,942,760,612,599,0]




 
    def scaled_range(self, distance, yield_):
        return distance * (1 / yield_) ** (1 / 3) * (self.ambient_pressure / 14.7) ** (1 / 3)

    def distance_from_scaled_range(self, scaled_range, yield_):
        return scaled_range / ((1 / yield_) ** (1 / 3) * (self.ambient_pressure / 14.7) ** (1 / 3))

    def yield_from_scaled_range(self, scaled_range, distance):
        return 1 / ((scaled_range / distance / (self.ambient_pressure / 14.7) ** (1 / 3)) ** 3)

    def scaled_yield(self, yield_, ref_distance, ref_yield):
        return ref_distance / ((ref_yield / yield_) ** (1 / 3))

    def initial_nuclear_radiation(self, distance, yield_, airburst):
        yieldscale = 1
        if yield_ < 1:
            yieldscale = 100
            yield_ = yield_ * yieldscale
            if yield_ < 10:
                scaling_factor = 1
            else:
                scaling_factor = self.eq_result('2-115', yield_)
            if airburst:
                surface = 1
                density_ratio = 0.9
            else:
                surface = 2 / 3
                density_ratio = 1

    def eq_2_116(self, yield_, distance, density_ratio, surface, scaling_factor, yieldscale):
        r = (yield_ / pow(distance, 2)) * (
                4997.41 * exp(-9.263158 * (density_ratio) * distance) + (surface * 1033) * (
                scaling_factor) * exp(-5.415384 * (density_ratio) * distance))
        return r / yieldscale

    def initial_nuclear_radiation_distance(self, yield_, rem, airburst):
        if rem >= 1 and rem <= pow(10, 8):
            a = +0.1237561
            a_ = +0.0143624
            b = +0.0994027
            b_ = -0.0000816
            c = +0.0011878
            c_ = -0.0000014
            d = -0.0002481
            d_ = +0.0054734
            e = +0.0000096
            e_ = -0.0003272
            f = -0.1308215
            f_ = +0.0000106
            g = +0.0009881
            g_ = -0.0001220
            h = -0.0032363
            h_ = +0.0000217
            i = +0.0000111
            i_ = -0.0000006

            logI = self.log10(rem)
            logI2 = pow(logI, 2)
            logI3 = pow(logI, 3)
            self.log10(yield_)
            self.logW = self.log10(yield_)

            #
            distance = a + (b + a_ * logI + d_ * logI2 + g_ * logI3) * self.logW
            distance += (c + b_ * logI + e_ * logI2 + h_ * logI3) * pow(self.logW, 3)
            distance += (d + (c_ * logI) + (f_ * logI2) + (i_ * logI3)) * pow(self.logW, 5)
            distance += (e * pow(self.logW, 7)) + (f * logI) + (g * logI2) + (h * logI3)
            distance += (i * pow(logI, 5))

            return pow(10, distance)
        else:
            self.error = "REM OUTSIDE RANGE [rem: " + str(rem) + ", min: " + str(1) + ", max: " + str(pow(10, 8)) + "]"
            if self.debug:
                print(self.error)

            return False

    def fireball_radius(self, yield_, hob_ft):
        if yield_ is None:
            self.error = "MISSING INPUT PARAMETER"
            if self.debug:
                print(self.error)

            return None

        contact_burst = 145 * pow(yield_, 0.4) * 4
        air_burst = 110 * pow(yield_, 0.4) * 4

        self.contact_burst_hob = 5 * pow(yield_, 0.3)
        self.air_burst_hob = 180 * pow(yield_, .4)

        if hob_ft <= self.contact_burst_hob:
            return contact_burst * ft2mi
        if hob_ft <= self.air_burst_hob:
            print(self.lerp)
            return self.lerp(contact_burst, self.contact_burst_hob, air_burst, self.air_burst_hob, hob_ft) * ft2mi
        return air_burst * ft2mi



    def switch(self, airburst):
        if airburst is False:
            return .04924 * pow(self.yield_, .4)
        elif airburst is True:
            return .03788 * pow(self.yield_, .4)
        else:
            return .04356 * pow(self.yield_, .4)

    def minimum_height_for_negligible_fallout(self, yield_):
        if yield_ is None:
            self.error = "MISSING INPUT PARAMETER"
            if self.debug:
                print(self.error)
            return None
        return .03409 * pow(yield_, .4)

    def crater(self, yield_, soil):
        if yield_ is None:
            self.error = "MISSING INPUT PARAMETER"
            if self.debug:
                print(self.error)
            return None
        c = []
        if soil:
            c.append(.02398 * pow(yield_, 1 / 3))
            c.append(.01199 * pow(yield_, 1 / 3))
            c.append(.005739 * pow(yield_, 1 / 3))
        else:
            c.append(.01918 * pow(yield_, 1 / 3))
            c.append(.009591 * pow(yield_, 1 / 3))
            c.append(.004591 * pow(yield_, 1 / 3))
        return c

    def thermal_radiation_q(self, distance, yield_, airburst):
        y = self.eq_result('2-106', distance)
        if yield_ < 1:
            kt = yield_ * 1000
            scale = .001
        elif yield_ > 20000:
            kt = yield_ / 10
            scale = 10
        else:
            kt = yield_
            scale = 1
        if airburst:
            return (y / (1 / kt)) * scale
        else:
            return (y / (1 / (.7 * kt))) * scale

    def thermal_radiation_distance(self, radiation, yield_, airburst):
        if airburst:
            return self.eq_result('2-108', radiation * (1 / yield_))
        else:
            return self.eq_result('2-108', radiation * (1 / (.7 * yield_)))

    def thermal_radiation_param_q(self, yield_, param):
        if param == '_1st-50':
            return math.log(self.eq_result('77-12.65-1st-50', yield_, math.e, True))
        elif param == '_2nd-50':
            return math.log(self.eq_result('77-12.65-2nd-50', yield_, math.e, True))
        elif param == '_3rd-50':
            return math.log(self.eq_result('77-12.65-3rd-50', yield_, math.e, True))
        elif param == '_3rd-100':
            return math.log(self.eq_result('77-12.65-3rd-100', yield_, math.e, True))
        elif param == '_noharm-100':
            return math.log(self.eq_result('77-12.65-noharm-100', yield_, math.e, True))
        else:
            self.error = "MISSING PARAM"
            if self.debug:
                print(self.error)
            return None

    def thermal_radiation_1st_q(self, yield_):
        return self.eq_result('2-110', yield_)

    def thermal_radiation_2nd_q(self, yield_):
        return self.eq_result('2-111', yield_)

    def optimum_height_of_burst_from_overpressure(self, yield_, maximum_overpressure):
        return self.eq_result('2-78', maximum_overpressure) / pow(self.ambient_pressure / 14.7, 1 / 3) / pow(1 / yield_, 1 / 3)

    def optimum_height_of_burst(self, distance, yield_):
        return self.eq_result('2-79', distance * pow(1 / yield_, 1 / 3) * pow(self.ambient_pressure / 14.7, 1 / 13)) / pow(
            self.ambient_pressure / 14.7, 1 / 3) / pow(1 / yield_, 1 / 3)

    def maximum_overpressure_range(self, x, airburst):
        if x is None:
            self.error = "MISSING X PARAMETER"
            if self.debug:
                print(self.error)
            return None
        if airburst is None:
            self.error = "NO HEIGHT OF BURST DEFINED"
            if self.debug:
                print(self.error)
            return None
        if airburst is False:
            return self.eq_result('2-5', x)
        elif airburst is True:
            return self.eq_result('2-61', x)

    def maximum_overpressure_psi(self, x, airburst):
        if x is None:
            self.error = "MISSING X PARAMETER"
            if self.debug:
                print(self.error)
            return None
        if airburst is None:
            self.error = "NO HEIGHT OF BURST DEFINED"
            if self.debug:
                print(self.error)
            return None
        if airburst is False:
            return self.eq_result('2-4', x)
        elif airburst is True:
            return self.eq_result('2-60', x)

    def maximum_dynamic_pressure_psi(self, x, airburst):
        if x is None:
            self.error = "MISSING X PARAMETER"
            if self.debug:
                print(self.error)
            return None
        if airburst is None:
            self.error = "NO HEIGHT OF BURST DEFINED"
            if self.debug:
                print(self.error)
            return None
        if airburst is False:
            return self.eq_result('2-6', x)
        elif airburst is True:
            if x < .154:
                return self.eq_result('2-64', x)
            else:
                return self.eq_result('2-62', x)

    def duration_positive_overpressure(self, x, airburst):
        if x is None:
            self.error = "MISSING X PARAMETER"
            if self.debug:
                print(self.error)
            return None
        if airburst is None:
            self.error = "NO HEIGHT OF BURST DEFINED"
            if self.debug:
                print(self.error)
            return None
        if airburst is False:
            return self.eq_result('2-8', x)

    def blast_wave_arrival(self, x, airburst):
        if x is None:
            self.error = "MISSING X PARAMETER"
            if self.debug:
                print(self.error)
            return None
        if airburst is None:
            self.error = "NO HEIGHT OF BURST DEFINED"
            if self.debug:
                print(self.error)
            return None
        if airburst is False:
            return self.eq_result('2-12', x)

    def maximum_wind_velocity_mph(self, x, airburst):
        if x is None:
            self.error = "MISSING X PARAMETER"
            if self.debug:
                print(self.error)
            return None
        if airburst is None:
            self.error = "NO HEIGHT OF BURST DEFINED"
            if self.debug:
                print(self.error)
            return None
        if airburst is False:
            return self.eq_result('2-16', x)
        elif airburst is True:
            if x > 0.2568:
                return self.eq_result('2-74', x)
            else:
                return self.eq_result('2-76', x)


    def psi_distance(self, kt, psi, airburst):
        if kt > 20000:
            d = self.distance_from_scaled_range(self.maximum_overpressure_range(psi, airburst), kt / 1000)
            return d * 10
        elif kt < 1:
            d = self.distance_from_scaled_range(self.maximum_overpressure_range(psi, airburst), kt * 1000)
            return d / 10
        else:
            d = self.distance_from_scaled_range(self.maximum_overpressure_range(psi, airburst), kt)
            return d

    def ground_range_from_slant_range(self, slant_range, height):
        if slant_range < height:
            return 0
        else:
            return sqrt(pow(slant_range, 2) - pow(height, 2))

    def thermal_distance(self, kt, therm, airburst):
        if therm in ["_3rd-50", "_3rd-100", "_2nd-50", "_1st-50", "_noharm-100"]:
            if kt < 1:
                d1 = self.thermal_radiation_distance(self.thermal_radiation_param_q(1, therm), 1, airburst)
                d = self.scaled_yield(kt, d1, 1)
            elif kt > 20000:
                d1 = self.thermal_radiation_distance(self.thermal_radiation_param_q(kt, therm), 20000, airburst)
                d = self.scaled_yield(kt, d1, 20000)
            else:
                d = self.thermal_radiation_distance(self.thermal_radiation_param_q(kt, therm), kt, airburst)
            return d
        else:
            return self.thermal_radiation_distance(therm, kt, airburst)

    def range_from_psi_hob(self, kt, psi, hob):
        scaled_hob = hob / pow(kt, 1 / 3)
        range_at_1kt = self.range_from_psi_hob_1kt(psi, scaled_hob)
        return range_at_1kt * pow(kt, 1 / 3)


    psi_index = []

    for p in hobs.keys():
        psi_index.append(int(p))
    psi_index.sort()
    
    def make_smooth_hob_array(self):
          hobs_sm = {}
          rngs_sm = {}
          for psi in self.hobs:
              rv = -1
              hobs_sm[psi] = []
              rngs_sm[psi] = []
              for k in self.hobs[psi]:
                  if self.hobs[psi][k] > rv:
                      hobs_sm[psi].append(self.hobs[psi][k])
                      rngs_sm[psi].append(self.rngs[psi][k])
                      rv = self.hobs[psi][k]
          return hobs_sm, rngs_sm


    def max_height_for_psi(self, kt, psi):
         if psi in hobs:
             return hobs[psi][-1]
         else:
             psi_ = psi_find(psi)
             return self.lerp(self.max_height_for_psi(kt, psi_[0]), psi_[0], self.max_height_for_psi(kt, psi_[1]), psi_[1], psi)

    def range_from_psi_hob_1kt(self, psi, hob):
         if hob < 0 or psi > 10000 or psi < 1:
             return False
         if psi in hobs:
             if hob > hobs[psi][-1]:
                 return 0
             near_hobs = array_closest(hobs_sm[psi], hob)
             if len(near_hobs) == 1:
                 return rngs_sm[psi][near_hobs[0]]
             else:
                 min_hob_k = near_hobs[0]
                 max_hob_k = near_hobs[1]
             return self.lerp(rngs_sm[psi][min_hob_k], hobs_sm[psi][min_hob_k], rngs_sm[psi][max_hob_k], hobs_sm[psi][max_hob_k], hob)
         else:
             return range_from_psi_hob_1kt_interpolated(psi, hob)

    def range_from_psi_hob_1kt_interpolated(self, psi, hob):
         h = hob
         psi_ = psi_find(psi)
         p1 = psi_[0]
         p2 = psi_[1]
         if h <= 0:
             result = self.lerp(rngs[p1][0], p1, rngs[p2][0], p2, psi)
             return result
         max_hob_outer = hobs[p1][-1]
         max_hob_inner = hobs[p2][-1]
         max_hob_lerp = self.lerp(max_hob_outer, p1, max_hob_inner, p2, psi)
         if h > max_hob_lerp:
             return 0
         proportion = self.lerp(0, p2, 1, p1, psi)
         near_hobs = array_closest(hobs[p1], h)
         outer_index = near_hobs[0]
         search_direction = 1
         intercept = getInterpolatedPosition(p2, p1, outer_index)
         if not intercept:
             return False
         h_low_index = None
         h_low_prop = None
         r_low_prop = None
         h_high_index = None
         h_high_prop = None
         r_high_prop = None
         while intercept[1] < h:
             rng_at_prop = self.lerp(rngs[p1][outer_index], 1, intercept[0], 0, proportion)
             hob_at_prop = self.lerp(hobs[p1][outer_index], 1, intercept[1], 0, proportion)
             if hob_at_prop < h:
                 if outer_index > h_low_index or h_low_index is None:
                     h_low_index = outer_index
                     h_low_prop = hob_at_prop
                     r_low_prop = rng_at_prop
             if hob_at_prop > h:
                 if h_low_index:
                     h_high_prop = hob_at_prop
                     r_high_prop = rng_at_prop
                     result = self.lerp(r_low_prop, h_low_prop, r_high_prop, h_high_prop, h)
                     return result
                     break
             outer_index += search_direction

    def range_from_psi_hob_1kt_interpolated(self, psi, hob):
        h = hob
        psi_ = self.psi_find(psi)
        p1 = psi_[0]
        p2 = psi_[1]
        if h <= 0:
            result = self.lerp(rngs[p1][0], p1, rngs[p2][0], p2, psi)
            return result
        max_hob_outer = hobs[p1][-1]
        max_hob_inner = hobs[p2][-1]
        max_hob_lerp = self.lerp(max_hob_outer, p1, max_hob_inner, p2, psi)
        if h > max_hob_lerp:
            return 0
        proportion = self.lerp(0, p2, 1, p1, psi)
        near_hobs = self.array_closest(hobs[p1], h)
        outer_index = near_hobs[0]
        search_direction = 1
        intercept = self.getInterpolatedPosition(p2, p1, outer_index)
        if not intercept:
            return False
        while intercept[1] < h:
            rng_at_prop = self.lerp(rngs[p1][outer_index], 1, intercept[0], 0, proportion)
            hob_at_prop = self.lerp(hobs[p1][outer_index], 1, intercept[1], 0, proportion)
            if hob_at_prop < h:
                if outer_index > h_low_index or h_low_index is None:
                    h_low_index = outer_index
                    h_low_prop = hob_at_prop
                    r_low_prop = rng_at_prop
            if hob_at_prop > h:
                if h_low_index:
                    h_high_prop = hob_at_prop
                    r_high_prop = rng_at_prop
                    result = self.lerp(r_low_prop, h_low_prop, r_high_prop, h_high_prop, h)
                    return result
                    break
            outer_index += search_direction
            if outer_index >= len(hobs[p1]) or outer_index < 0:
                return False
            else:
                intercept = self.getInterpolatedPosition(p2, p1, outer_index)
                if not intercept:
                    return False
        if not result and h_low_index:
            rng_at_prop = self.lerp(rngs[p1][outer_index], 1, intercept[0], 0, proportion)
            hob_at_prop = self.lerp(hobs[p1][outer_index], 1, intercept[1], 0, proportion)
            h_high_prop = hob_at_prop
            r_high_prop = rng_at_prop
            result = self.lerp(r_low_prop, h_low_prop, r_high_prop, h_high_prop, h)
            return result
        else:
            rng_at_prop = self.lerp(rngs[p1][outer_index], 1, intercept[0], 0, proportion)
            hob_at_prop = self.lerp(hobs[p1][outer_index], 1, intercept[1], 0, proportion)
            h_high_prop = hob_at_prop
            r_high_prop = rng_at_prop
            intercept = self.getInterpolatedPosition(p2, p1, outer_index - 1)
            if not intercept:
                return False
            rng_at_prop = self.lerp(rngs[p1][outer_index - 1], 1, intercept[0], 0, proportion)
            hob_at_prop = self.lerp(hobs[p1][outer_index - 1], 1, intercept[1], 0, proportion)
            h_low_prop = hob_at_prop
            r_low_prop = rng_at_prop
            result = self.lerp(r_low_prop, h_low_prop, r_high_prop, h_high_prop, h)
            return result
        return False

    def getInterpolatedPosition(self, inner_psi, outer_psi, outer_index):
        inner_index = 0
        while not self.linesIntersect(
                0, 0,
                rngs[outer_psi][outer_index], hobs[outer_psi][outer_index],
                rngs[inner_psi][inner_index], hobs[inner_psi][inner_index],
                rngs[inner_psi][inner_index + 1], hobs[inner_psi][inner_index + 1]
        ):
            inner_index += 1
            if inner_index > len(rngs[inner_psi]) or inner_index - 1 < 0:
                return False
        return self.getLineLineIntersection(0, 0, rngs[outer_psi][outer_index], hobs[outer_psi][outer_index],
                                             rngs[inner_psi][inner_index + 1], hobs[inner_psi][inner_index + 1],
                                             rngs[inner_psi][inner_index], hobs[inner_psi][inner_index])

    def getLineLineIntersection(self, x1, y1, x2, y2, x3, y3, x4, y4):
        det1And2 = self.getLineLineIntersection_det(x1, y1, x2, y2)
        det3And4 = self.getLineLineIntersection_det(x3, y3, x4, y4)
        x1LessX2 = x1 - x2
        y1LessY2 = y1 - y2
        x3LessX4 = x3 - x4
        y3LessY4 = y3 - y4
        det1Less2And3Less4 = self.getLineLineIntersection_det(x1LessX2, y1LessY2, x3LessX4, y3LessY4)
        if det1Less2And3Less4 == 0:
            return False
        x = (self.getLineLineIntersection_det(det1And2, x1LessX2, det3And4, x3LessX4) / det1Less2And3Less4)
        y = (self.getLineLineIntersection_det(det1And2, y1LessY2, det3And4, y3LessY4) / det1Less2And3Less4)
        return [x, y]

    def getLineLineIntersection_det(self, a, b, c, d):
        return a * d - b * c
    def linesIntersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        if x1 == x2 and y1 == y2 or x3 == x4 and y3 == y4:
            return False
        ax = x2 - x1
        ay = y2 - y1
        bx = x3 - x4
        by = y3 - y4
        cx = x1 - x3
        cy = y1 - y3

        alphaNumerator = by * cx - bx * cy
        commonDenominator = ay * bx - ax * by
        if commonDenominator > 0:
            if alphaNumerator < 0 or alphaNumerator > commonDenominator:
                return False
        elif commonDenominator < 0:
            if alphaNumerator > 0 or alphaNumerator < commonDenominator:
                return False
        betaNumerator = ax * cy - ay * cx
        if commonDenominator > 0:
            if betaNumerator < 0 or betaNumerator > commonDenominator:
                return False
        elif commonDenominator < 0:
            if betaNumerator > 0 or betaNumerator < commonDenominator:
                return False
        if commonDenominator == 0:
            y3LessY1 = y3 - y1
            collinearityTestForP3 = x1 * (y2 - y3) + x2 * (y3LessY1) + x3 * (y1 - y2)
            if collinearityTestForP3 == 0:
                if x1 >= x3 and x1 <= x4 or x1 <= x3 and x1 >= x4 or x2 >= x3 and x2 <= x4 or x2 <= x3 and x2 >= x4 or x3 >= x1 and x3 <= x2 or x3 <= x1 and x3 >= x2:
                    if y1 >= y3 and y1 <= y4 or y1 <= y3 and y1 >= y4 or y2 >= y3 and y2 <= y4 or y2 <= y3 and y2 >= y4 or y3 >= y1 and y3 <= y2 or y3 <= y1 and y3 >= y2:
                        return True
            return False
        return True

    def array_max_value(self, array):
        return max(array)

    def array_keys(self, myObject, searchVal=None):
        output = []
        for key in myObject:
            if searchVal is not None:
                if myObject[key] == searchVal:
                    output.append(key)
            else:
                output.append(key)
        return output

    def array_closest(self, arr, val):
        lo = None
        hi = None
        for i in arr:
            if arr[i] == val:
                return [i]
            if arr[i] <= val and (lo is None or lo < arr[i]):
                lo = arr[i]
                lo_k = i
            if arr[i] >= val and (hi is None or hi > arr[i]):
                hi = arr[i]
                hi_k = i
        if hi_k != lo_k + 1:
            lo_k = hi_k - 1
        return [lo_k, hi_k]



    def psi_find(self, psi):
        min_psi = None
        max_psi = None
        for p in psi_index:
            if int(psi_index[p]) < psi:
                min_psi = psi_index[p]
            if int(psi_index[p]) > psi:
                if not max_psi:
                    max_psi = psi_index[p]
        return [min_psi, max_psi]

    def max_height_for_psi(self, kt, psi):
        if psi in hobs:
            max_hob = self.array_max_value(hobs[psi])
            return max_hob * pow(kt, 1 / 3)
        else:
            psi_ = self.psi_find(psi)
            max_hob_outer = hobs[psi_[0]][-1]
            max_hob_inner = hobs[psi_[1]][-1]
            return self.lerp(max_hob_outer, psi_[0], max_hob_inner, psi_[1], psi) * pow(kt, 1 / 3)

    def opt_height_for_psi(self, kt, psi):
        if psi in hobs:
            maxs = self.array_keys(rngs[psi], self.array_max_value(rngs[psi]))
            return hobs[psi][maxs[0]] * pow(kt, 1 / 3)
        else:
            psi_ = self.psi_find(psi)
            return self.lerp(self.opt_height_for_psi(kt, psi_[0]), psi_[0], self.opt_height_for_psi(kt, psi_[1]), psi_[1], psi)

    def psi_at_distance_hob(self, dist_ft, kt, hob):
        min_psi = None
        max_psi = None

        scaled_hob = hob / pow(kt, 1 / 3)
        scaled_dist = dist_ft / pow(kt, 1 / 3)

        dist_1psi = self.range_from_psi_hob(kt, 1, hob)
        dist_10000psi = self.range_from_psi_hob(kt, 10000, hob)
        if dist_1psi < dist_ft:
            return 0
        if dist_ft < dist_10000psi:
            return "+10,000"

        max_dist = dist_1psi
        min_dist = 0

        for psi in hobs.keys():
            psi_dist = self.range_from_psi_hob_1kt(psi, scaled_hob)
            if psi_dist == scaled_dist and psi_dist > 0:
                return psi
            elif psi_dist < scaled_dist:
                if psi_dist > min_dist:
                    min_dist = psi_dist
                    min_psi = psi
            elif psi_dist > scaled_dist:
                if psi_dist < max_dist:
                    max_dist = psi_dist
                    max_psi = psi

        if min_psi and max_psi:
            return self.lerp(max_psi, max_dist, min_psi, min_dist, scaled_dist)
        elif not min_psi and max_psi:
            psi_ = self.psi_find(max_psi, max_psi + 1)
            min_psi = psi_[1]
            near_rngs = self.array_closest(rngs[min_psi], scaled_dist)
            min_dist = hobs[min_psi][near_rngs[0]]
            near_rngs = self.array_closest(rngs[max_psi], scaled_dist)
            max_dist = hobs[max_psi][near_rngs[0]]

            if not min_psi:
                return "10000"
            return self.lerp(max_psi, max_dist, min_psi, min_dist, scaled_hob)



    def accumulated_dose_rate(self, rads, hours):
        dose_rate_x = 150
        hour_x = 2188
        accumulated_x = 1260

        dose_rate_y = -8.5763502429382902E+02 + 3.6396739040111243E+02 * log(1.0721058158242694E+02 * rads) - 2.5144779874708423E-01 * pow(log(1.0721058158242694E+02 * rads), 2)
        hour_y = -8.5763502429382902E+02 + 3.6396739040111243E+02 * log(1.0721058158242694E+02 * hours) - 2.5144779874708423E-01 * pow(log(1.0721058158242694E+02 * hours), 2)

        accumulated_y = dose_rate_y + (accumulated_x - dose_rate_x) * ((hour_y - dose_rate_y) / (hour_x - dose_rate_x))

        accumulated = abs(round((-6.5590188579167236E-02 * (accumulated_y) + 5.4538196288120129E-05 * (pow(accumulated_y, 2))) / (1.0 + -4.9969343147258514E+03 * (pow(accumulated_y, -1)) + 6.3089179198324122E+06 * (pow(accumulated_y, -2))), 2))

        return accumulated

    def cloud_initial_radius(self, yield_):
        if 0 < yield_ <= 100000:
            return 2.09 * pow(10, 2) * pow(yield_, .333)
        else:
            self.error = "YIELD OUTSIDE OF BOUNDS"
            if self.debug:
                print(self.error)
            return None

    def cloud_final_horizontal_semiaxis(self, yield_):
        if 0 < yield_ <= 100000:
            return 2.34 * pow(10, 3) * pow(yield_, .431)
        else:
            self.error = "YIELD OUTSIDE OF BOUNDS"
            if self.debug:
                print(self.error)
            return None

    def cloud_final_vertical_semiaxis(self, yield_):
        if 0 < yield_ <= 100000:
            return 1.40 * pow(10, 3) * pow(yield_, .431)
        else:
            self.error = "YIELD OUTSIDE OF BOUNDS"
            if self.debug:
                print(self.error)
            return None

    def cloud_final_height(self, yield_):
        if 0 < yield_ <= 100000:
            if yield_ <= 28:
                return 0.66 * pow(10, 4) * pow(yield_, .445)
            else:
                return 1.68 * pow(10, 4) * pow(yield_, .164)
        else:
            self.error = "YIELD OUTSIDE OF BOUNDS"
            if self.debug:
                print(self.error)
            return None

    def cloud_horizonal_semiaxis_at_altitude(self, altitude, cloud_final_height, cloud_initial_radius, cloud_final_horizontal_semiaxis):
        h = cloud_final_height
        R_s = cloud_initial_radius
        a = cloud_final_horizontal_semiaxis
        a_o = pow(10, log10(a) - (h * log10(a / R_s)) / (h - R_s))
        k_a = 2.303 * (log10(a / R_s) / (h - R_s))
        return a_o * pow(e, (k_a * altitude))

    def cloud_vertical_semiaxis_at_altitude(self, altitude, cloud_final_height, cloud_final_vertical_semiaxis, cloud_initial_radius):
        h = cloud_final_height
        b = cloud_final_vertical_semiaxis
        R_s = cloud_initial_radius
        b_o = pow(10, log10(b) - (h * log10(b / R_s)) / (h - R_s))
        k_b = 2.303 * (log10(b / R_s) / (h - R_s))
        return b_o * pow(e, (k_b * altitude))

    def cloud_rate_of_rise_bottom(self, height_of_center, vertical_semiaxis, time_after_detonation):
        return (height_of_cloud - vertical_semiaxis) * (1 - pow(e, -.0123 * time_after_detonation))
     
    def cloud_rate_of_rise_top(self, height_of_center, vertical_semiaxis, time_after_detonation):
         if time_after_detonation < 20:
             return .331 * (height_of_center - vertical_semiaxis) * (1 - exp(-.0626 * time_after_detonation))
         else:
             return .893 * (height_of_center - vertical_semiaxis) * (1.120 - exp(-.00784 * time_after_detonation))

    def cloud_rate_of_rise_center(self, height_of_center, time_after_detonation):
         return .915 * height_of_center * (1.093 - exp(-.00905 * time_after_detonation))

    def cloud_top_height_percent_at_time(self, seconds):
         if seconds >= 270:
             return 1
         else:
             return 9.7225115080563657E-03 + 7.9925510016408026E-03 * seconds - 1.8866872395194888E-05 * pow(seconds, 2) + 1.0765594837466863E-08 * pow(seconds, 3)

    def cloud_time_until_maximum_height(self, yield_):
         pass

    def cloud_bottom(self, yield_):
         return 1000 * (1.7154976807456771E+02 * pow(yield_ / 5.2402966478808509E+05, 2.5445292192920910E-01) * exp(yield_ / 5.2402966478808509E+05) - 3.2665357749287349E-01)

    def cloud_top(self, yield_):
         if yield_ <= 100:
             return 1000 * (9.0355598798544854E+00 * pow(yield_, 3.2095070520890268E-01 - 4.7081309288753766E-05 * yield_) + 8.1777330384279173E-02)
         elif yield_ <= 4000:
             return 1000 * (2.3037246630847605E+01 * pow(yield_, 1.5119655810555122E-01 - 4.6347426409373220E+00 / yield_) + 1.4709881303279233E+00)
         else:
             return 1000 * (6.5357594810058774E+00 * pow(1.0817408033549503E+288, 1.0 / yield_) * pow(yield_, 2.8416073403767877E-01))


    def eq_result(self, eq_id, x, logbase=None, ignore_range=False):
        if eq_id in self.eq:
            if x is None:
                self.error = "X UNDEFINED FOR EQ." + eq_id
                if self.debug:
                    print(self.error)
                return None
            elif (x < self.eq[eq_id]['xmin'] or x > self.eq[eq_id]['xmax']) and (not ignore_range):
                self.error = "X OUTSIDE RANGE FOR EQ." + eq_id + " [x: " + str(x) + ", xmin: " + str(self.eq[eq_id]['xmin']) + ", xmax: " + str(self.eq[eq_id]['xmax']) + "]"
                if self.debug:
                    print(self.error)
                return False
            else:
                return self.loggo(x, self.eq[eq_id]['args'], logbase)
        else:
            self.error = "EQUATION NOT FOUND [eq_id: " + eq_id + "]"
            if self.debug:
                print(self.error)
            return None

    def loggo(self, x, args, logbase=None):
         l = 0
         if not logbase:
             logbase = 10
         logbx = log(float(x), logbase)

         for i in range(len(args)):
             l += args[i] * pow(logbx, i)
         return pow(logbase, l)

    def poly(self, x, args):
         l = 0
         for i in range(len(args)):
             l += args[i] * pow(x, i)
         return l

    def log10(self, n):
         return log(n, 10)


    def logb(n, base):
        if base == e:
            return log(n)
        elif base == 10:
            return log10(n)
        elif base == 2:
            return log2(n)
        else:
            return log(n, base)

    def pow(n, x):
        return pow(n, x)

    @staticmethod
    def lerp(x1, y1, x2, y2, y3):
           if y2 == y1:
               return False
           else:
               return ((y2 - y3) * x1 + (y3 - y1) * x2) / (y2 - y1)

    def inArray(needle, haystack):
        return needle in haystack




    def set_debug(self, status):
        self.debug = status
        print("DEBUG = ", status)



bc = NukeEffects()
ft2mi = 0.000189394



yield_ = float(input('Please enter the yield of the explosion (in kilotons): '))
soil = input('Is the ground soil? (yes/no): ').lower() == 'yes'
  
craterDimensions = bc.crater(yield_, soil)
print("The depth of the crater is: " + str(craterDimensions[2]) + " miles")
print("The lip radius of the crater is: " + str(craterDimensions[0]) + " miles")
print("The apparent radius of the crater is: " + str(craterDimensions[1]) + " miles")

yield_ = float(input('Please enter the yield of the explosion: '))
airburst = input('Is the explosion an airburst? (yes/no): ').lower() == 'yes'
bc = NukeEffects()
bc.fireball_radius(yield_, 0)  # Call this method to set air_burst_hob and contact_burst_hob
hob_ft = bc.air_burst_hob if airburst else bc.contact_burst_hob
radius = bc.fireball_radius(yield_, hob_ft)
print("The fireball radius is: " + str(radius) + " miles")

yield_ = float(input('Please enter the yield of the explosion: '))
bc = NukeEffects()
airburst = True
remLevels = [100, 500, 600, 1000, 5000]
for i in range(len(remLevels)):
    distance = bc.initial_nuclear_radiation_distance(yield_, remLevels[i], airburst)
    print("Radiation level: " + str(remLevels[i]) + " rem, Distance: " + str(distance) + " miles")   


yield_ = float(input('Enter the yield of the explosion in kilotons: '))
answer = input('Is it an airburst? (yes/no): ')
airburst = (answer.lower() == 'yes')
bc = NukeEffects()
distance_1st_degree = bc.thermal_distance(yield_, "_1st-50", airburst)
print("Distance for 1st degree burns: " + str(distance_1st_degree) + " miles")
distance_no_harm = bc.thermal_distance(yield_, "_noharm-100", airburst)
print("Distance for no harm: " + str(distance_no_harm) + " miles") 

overpressure = float(input('Enter the overpressure you want (in psi): '))
burstType = input('Enter the type of burst you want (airburst or groundburst): ')
yield_ = float(input('Enter the yield of the explosion (in kilotons): '))
isAirburst = (burstType.lower() == "airburst")
scaledRange = bc.maximum_overpressure_range(overpressure, isAirburst)
distance = bc.distance_from_scaled_range(scaledRange, yield_)
print("The distance for the given overpressure, burst type, and yield is: " + str(distance) + " units.")


yield_ = float(input('Enter the yield of the explosion (in kilotons): '))


cloud_altitude = bc.cloud_final_height(yield_)
cloud_head_radius = bc.cloud_final_horizontal_semiaxis(yield_)
cloud_head_height = bc.cloud_final_vertical_semiaxis(yield_)


print("Mushroom cloud altitude: " + str(cloud_altitude) + " units.")
print("Mushroom cloud head radius: " + str(cloud_head_radius) + " units.")
print("Mushroom cloud head height: " + str(cloud_head_height) + " units.")


