##
# @file changeCalibrationData.py
# @brief Change Kalibr Calibration data to FirmwareData2
# @author Yang Sen, magicys@qq.com
# @version 1.0.0
# @date 2017-06-14

import sys,os

def readKalibrImuCalibrationDataFile(file_name, baseline = '50'):
    calibration_data = {'cam0': {'T_ci': "", 'timeshift': "", 'Focal length': "", 'Principal point': "", 'Distortion coefficients': "" }, 'cam1': {'T_ci': "", 'timeshift': "", 'Focal length': "", 'Principal point': "", 'Distortion coefficients': ""}, 'Image Size': "640 480", 'Baseline': baseline}
    fin = open(file_name, 'r')
    lines = fin.readlines()
    fin.close()
    i = 0
    while i < len(lines):
        line = lines[i]
        if 'T_ci' in line:
            if 'cam0' in line:
                j = 1
                str_temp = line
                while i + j < len(lines) and j < 4:
                    temp = lines[i+j].strip('\n').split(' ')
                    num_title = []
                    for k in range(0, len(temp)):
                        kk = temp[k].strip('[').strip(']').strip(' ')
                        if len(kk) != 0:
                            num_title.append(kk)
                    num_title[3] = str(1000 * float(num_title[3]))
                    str_temp = str_temp + '[' + " ".join(num_title) + ']\n'
                    j = j + 1

                calibration_data['cam0']['T_ci'] = str_temp
            elif 'cam1' in line:
                j = 1
                str_temp = line
                while i + j < len(lines) and j < 4:
                    temp = lines[i+j].strip('\n').split(' ')
                    num_title = []
                    for k in range(0, len(temp)):
                        kk = temp[k].strip('[').strip(']').strip(' ')
                        if len(kk) != 0:
                            num_title.append(kk)
                    num_title[3] = str(1000 * float(num_title[3]))
                    str_temp = str_temp + '[' + " ".join(num_title) + ']\n'
                    j = j + 1
                calibration_data['cam1']['T_ci'] = str_temp
            i = i + j
        elif 'timeshift' in line:
           if 'cam0' in line:
                j = 0
                str_temp = ""
                while i + j < len(lines) and j < 2:
                    str_temp = str_temp + lines[i+j]
                    j = j + 1
                calibration_data['cam0']['timeshift'] = str_temp
           elif 'cam1' in line:
                j = 0
                str_temp = ""
                while i + j < len(lines) and j < 2:
                    str_temp = str_temp + lines[i+j]
                    j = j + 1
                calibration_data['cam1']['timeshift'] = str_temp
           i = i + j
        elif line.strip('\n') == 'cam0':
           j = 2
           while i + j < len(lines) and j < 7:
                new_line = lines[i + j]
                if 'Focal length' in new_line:
                    calibration_data['cam0']['Focal length'] = new_line.split(':')[-1].strip(' ')
                elif 'Principal point' in new_line:
                    calibration_data['cam0']['Principal point'] = new_line.split(':')[-1].strip(' ')
                elif 'Distortion coefficients' in new_line:
                    calibration_data['cam0']['Distortion coefficients'] = new_line.split(':')[-1].strip(' ')
                j = j + 1
           i = i + j
        elif line.strip('\n') == 'cam1':
           j = 2
           while i + j < len(lines) and j < 7:
                new_line = lines[i + j]
                if 'Focal length' in new_line:
                    calibration_data['cam1']['Focal length'] = new_line.split(':')[-1].strip(' ')
                elif 'Principal point' in new_line:
                    calibration_data['cam1']['Principal point'] = new_line.split(':')[-1].strip(' ')
                elif 'Distortion coefficients' in new_line:
                    calibration_data['cam1']['Distortion coefficients'] = new_line.split(':')[-1].strip(' ')
                j = j + 1
           i = i + j
        else:
           i = i + 1
    return calibration_data

def printToFirmwareData(calibration_data, firmware2_file):
    fout = open(firmware2_file, 'w')
    fout.write(calibration_data['Image Size'] + "\n")
    fout.write(calibration_data['Baseline'] + "\n\n")
    fout.write('cam0' + "\n")
    fout.write(calibration_data['cam0']['T_ci'] + "\n")
    timeshift_title = calibration_data['cam0']['timeshift'].split('\n')
    fout.write(timeshift_title[0] + '\n[' + timeshift_title[1] + "]\n\n")
    fout.write('Focal length:' + "\n")
    fout.write(calibration_data['cam0']['Focal length'])
    fout.write('Principal point:' + "\n")
    fout.write(calibration_data['cam0']['Principal point'])
    fout.write('Distortion coefficients:' + "\n")
    fout.write('[0, ' + calibration_data['cam0']['Distortion coefficients'].strip('[') + "\n")
    fout.write('cam1' + "\n")
    fout.write(calibration_data['cam1']['T_ci'] + "\n")
    timeshift_title = calibration_data['cam1']['timeshift'].split('\n')
    fout.write(timeshift_title[0] + '\n[' + timeshift_title[1] + "]\n\n")
    fout.write('Focal length:' + "\n")
    fout.write(calibration_data['cam1']['Focal length'] + "\n")
    fout.write('Principal point:' + "\n")
    fout.write(calibration_data['cam1']['Principal point'] + "\n")
    fout.write('Distortion coefficients:' + "\n")
    fout.write('[0, ' + calibration_data['cam1']['Distortion coefficients'].strip('[') + "\n")
    fout.close()

    


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print '<fin_kalibr_calibration_data> <fout_firmware2_data>'
        sys.exit()
    kalibr_file = sys.argv[1]
    firmware2_file = sys.argv[2]
    calibration_data = readKalibrImuCalibrationDataFile(kalibr_file)
    printToFirmwareData(calibration_data, firmware2_file)
    

