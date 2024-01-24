def findDecision(obj): #obj[0]: NumWaitingJob, obj[1]: STime_A_VS_B, obj[2]: STime_A_VS_B_Diff, obj[3]: PTime_A_VS_B, obj[4]: PTime_A_VS_B_Diff, obj[5]: CompTime_A_VS_B, obj[6]: CompTime_A_VS_B_Diff, obj[7]: Start_A_VS_B, obj[8]: Start_A_VS_B_Diff, obj[9]: Tardy_A_VS_B, obj[10]: Tardy_A_VS_B_Diff
   # {"feature": "STime_A_VS_B_Diff", "instances": 828, "metric_value": 8.0042, "depth": 1}
   if obj[2]<=14.690821256038648:
      # {"feature": "PTime_A_VS_B_Diff", "instances": 447, "metric_value": 2.3002, "depth": 2}
      if obj[4]<=14.798953242956557:
         # {"feature": "Tardy_A_VS_B_Diff", "instances": 375, "metric_value": 1.0962, "depth": 3}
         if obj[10]<=204.03541016890688:
            # {"feature": "STime_A_VS_B", "instances": 365, "metric_value": 0.9074, "depth": 4}
            if obj[1] == '<':
               # {"feature": "Start_A_VS_B_Diff", "instances": 179, "metric_value": 1.7789, "depth": 5}
               if obj[8]>-46.09497206703911:
                  return 62.19
               elif obj[8]<=-46.09497206703911:
                  return 89.72151898734177
               else:
                  return 74.34078212290503
            elif obj[1] == '=':
               # {"feature": "NumWaitingJob", "instances": 100, "metric_value": 2.2553, "depth": 5}
               if obj[0]<=17:
                  return 73.06756756756756
               elif obj[0]>17:
                  return 104.3076923076923
               else:
                  return 81.19
            elif obj[1] == '>':
               # {"feature": "PTime_A_VS_B", "instances": 86, "metric_value": 3.9863, "depth": 5}
               if obj[3] == '>':
                  return 114.44
               elif obj[3] == '<':
                  return 70.73076923076923
               elif obj[3] == '=':
                  return 101.5
               else:
                  return 99.72093023255815
            else:
               return 82.1972602739726
         elif obj[10]>204.03541016890688:
            # {"feature": "CompTime_A_VS_B_Diff", "instances": 10, "metric_value": 34.3158, "depth": 4}
            if obj[6]>207:
               # {"feature": "Start_A_VS_B_Diff", "instances": 8, "metric_value": 17.3729, "depth": 5}
               if obj[8]>256:
                  return 157.4
               elif obj[8]<=256:
                  return 203.33333333333334
               else:
                  return 174.625
            elif obj[6]<=207:
               return 5
            else:
               return 140.7
         else:
            return 83.75733333333334
      elif obj[4]>14.798953242956557:
         # {"feature": "Tardy_A_VS_B_Diff", "instances": 72, "metric_value": 9.0582, "depth": 3}
         if obj[10]<=108:
            # {"feature": "STime_A_VS_B", "instances": 67, "metric_value": 3.9509, "depth": 4}
            if obj[1] == '=':
               # {"feature": "NumWaitingJob", "instances": 31, "metric_value": 6.4348, "depth": 5}
               if obj[0]<=17:
                  return 93.76190476190476
               elif obj[0]>17:
                  return 143.8
               else:
                  return 109.90322580645162
            elif obj[1] == '<':
               # {"feature": "Tardy_A_VS_B", "instances": 24, "metric_value": 13.3352, "depth": 5}
               if obj[9] == '=':
                  return 122.75
               elif obj[9] == '<':
                  return 98.875
               elif obj[9] == '>':
                  return 21.0
               else:
                  return 97.83333333333333
            elif obj[1] == '>':
               # {"feature": "CompTime_A_VS_B_Diff", "instances": 12, "metric_value": 42.5863, "depth": 5}
               if obj[6]>20:
                  return 108.0
               elif obj[6]<=20:
                  return 244.2
               else:
                  return 164.75
            else:
               return 115.40298507462687
         elif obj[10]>108:
            # {"feature": "NumWaitingJob", "instances": 5, "metric_value": 60.5045, "depth": 4}
            if obj[0]<=8:
               return 202.66666666666666
            elif obj[0]>8:
               return 355.0
            else:
               return 263.6
         else:
            return 125.69444444444444
      else:
         return 90.51230425055928
   elif obj[2]>14.690821256038648:
      # {"feature": "PTime_A_VS_B_Diff", "instances": 381, "metric_value": 6.6467, "depth": 2}
      if obj[4]<=14.62845086671857:
         # {"feature": "Start_A_VS_B", "instances": 309, "metric_value": 4.5434, "depth": 3}
         if obj[7] == '>':
            # {"feature": "NumWaitingJob", "instances": 186, "metric_value": 3.5362, "depth": 4}
            if obj[0]>8:
               # {"feature": "Tardy_A_VS_B_Diff", "instances": 134, "metric_value": 5.765, "depth": 5}
               if obj[10]<=24.455223880597014:
                  return 116.5934065934066
               elif obj[10]>24.455223880597014:
                  return 173.13953488372093
               else:
                  return 134.73880597014926
            elif obj[0]<=8:
               # {"feature": "Tardy_A_VS_B_Diff", "instances": 52, "metric_value": 5.6687, "depth": 5}
               if obj[10]>75.67672701864377:
                  return 100.21428571428571
               elif obj[10]<=75.67672701864377:
                  return 41.1
               else:
                  return 88.84615384615384
            else:
               return 121.90860215053763
         elif obj[7] == '<':
            # {"feature": "Start_A_VS_B_Diff", "instances": 117, "metric_value": 3.5572, "depth": 4}
            if obj[8]<=-5.013995550096681:
               # {"feature": "NumWaitingJob", "instances": 103, "metric_value": 3.9541, "depth": 5}
               if obj[0]>3:
                  return 175.37755102040816
               elif obj[0]<=3:
                  return 62.6
               else:
                  return 169.90291262135923
            elif obj[8]>-5.013995550096681:
               # {"feature": "Tardy_A_VS_B_Diff", "instances": 14, "metric_value": 29.3995, "depth": 5}
               if obj[10]<=17:
                  return 61.44444444444444
               elif obj[10]>17:
                  return 167.8
               else:
                  return 99.42857142857143
            else:
               return 161.47008547008548
         elif obj[7] == '=':
            # {"feature": "CompTime_A_VS_B_Diff", "instances": 6, "metric_value": 22.0787, "depth": 4}
            if obj[6]<=33:
               # {"feature": "Tardy_A_VS_B", "instances": 5, "metric_value": 1.4222, "depth": 5}
               if obj[9] == '=':
                  return 265.0
               elif obj[9] == '>':
                  return 261
               else:
                  return 264.2
            elif obj[6]>33:
               return 346
            else:
               return 277.8333333333333
         else:
            return 139.915857605178
      elif obj[4]>14.62845086671857:
         # {"feature": "NumWaitingJob", "instances": 72, "metric_value": 7.8317, "depth": 3}
         if obj[0]>7:
            # {"feature": "Tardy_A_VS_B_Diff", "instances": 56, "metric_value": 13.7031, "depth": 4}
            if obj[10]<=84.26589006816093:
               # {"feature": "CompTime_A_VS_B_Diff", "instances": 47, "metric_value": 11.4909, "depth": 5}
               if obj[6]>5.571354618158026:
                  return 203.60526315789474
               elif obj[6]<=5.571354618158026:
                  return 309.3333333333333
               else:
                  return 223.85106382978722
            elif obj[10]>84.26589006816093:
               # {"feature": "Start_A_VS_B_Diff", "instances": 9, "metric_value": 45.4455, "depth": 5}
               if obj[8]<=62:
                  return 431.8333333333333
               elif obj[8]>62:
                  return 215.33333333333334
               else:
                  return 359.6666666666667
            else:
               return 245.67857142857142
         elif obj[0]<=7:
            # {"feature": "Start_A_VS_B_Diff", "instances": 16, "metric_value": 5.9115, "depth": 4}
            if obj[8]>119:
               # {"feature": "CompTime_A_VS_B_Diff", "instances": 9, "metric_value": 25.9533, "depth": 5}
               if obj[6]>209:
                  return 196.66666666666666
               elif obj[6]<=209:
                  return 103.66666666666667
               else:
                  return 165.66666666666666
            elif obj[8]<=119:
               # {"feature": "CompTime_A_VS_B_Diff", "instances": 7, "metric_value": 6.1003, "depth": 5}
               if obj[6]>74:
                  return 188.83333333333334
               elif obj[6]<=74:
                  return 226
               else:
                  return 194.14285714285714
            else:
               return 178.125
         else:
            return 230.66666666666666
      else:
         return 157.06561679790028
   else:
      return 121.13647342995169
