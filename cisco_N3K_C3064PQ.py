import sqlite3
import re



class cisco_N3K_C3064PQ:
    def __init__(self,file):
        #variable constructor
        self.file = file
        #read all things in file
        read_file = open(self.file,'r')
        read_file_list = read_file.readlines()
        for line in read_file_list:
            #SOFTWARE TABLE
            #get device name
            if re.findall('^hostname (.*)',line):
                devicename = re.findall('^hostname (.*)',line)
                devicename = devicename[0]
                break
        for line in read_file_list:
            #get device model
            if re.findall('^.Product\sNumber\s+:+\s+(\S+)',line):
                model = re.findall('^.Product\sNumber\s+:+\s+(\S+)',line)
                model = model[0]
                break                
        for line in read_file_list:
            #get ios version
            if re.findall('^.*system image file is:\s+(\S+.bin)',line):
                iosversion = re.findall('^.*system image file is:\s+(\S+.bin)',line)
                iosversion = iosversion[0]
                break
        for line in read_file_list:
            #get uptime
            if re.findall('^.*uptime is (.*)',line):
                uptime = re.findall('^.*uptime is (.*)',line)
                uptime = uptime[0]
                break

        
        #get configuration register
        confreg = '-'

        for line in read_file_list:
            #SOFTWARE TABLE SUMMARY
            if re.findall('^.*system:\s+version\s+(\d+.\d+\S+)',line):
                version = re.findall('^.*system:\s+version\s+(\d+.\d+\S+)',line)
                version = version[0]
                break
        #print('\nversion : ', version )
        #print('\nnama device:', devicename)
        #print('\ndevice model: ', model)
        #print('\nios version: ', iosversion)
        #print('\nuptime: ', uptime)

        list_card = []
        list_serial_number = []
        list_hardware_description = []
        hardware_break = False
        for line in read_file_list:
            #HARDWARE
            #card PID
            if re.findall('^PID: (.*),.*,',line):
                hardware_break = True
                card = re.findall('^PID: (.*),.*,',line)
                card = card[0]
                list_card.append(card)
                
            #card serial number
            if re.findall('^PID: .*,.*,.*SN: (.*)',line):
                serial_number = re.findall('^PID: .*,.*,.*SN: (.*)',line)
                serial_number = serial_number[0]
                list_serial_number.append(serial_number)
                
            #description
            if re.findall('.*DESCR:\s+"(.*)"',line):
                hardware_description = re.findall('.*DESCR:\s+"(.*)"',line)
                hardware_description = hardware_description[0]
                list_hardware_description.append(hardware_description)
               
            #break loop
            if hardware_break == True and re.findall('.*#',line):
                break
        #print('\n\ndaftar list card :', list_card)
        #print('\n\ndaftar list serial number : ', list_serial_number)
        #print('\n\ndaftar list hardware desc : ', list_hardware_description)
        
        cpu_break = False
        for line in read_file_list:
            #CPU
            #cpu
            if re.findall('^CPU\sstates\s+:+\s+(\d.\d+)',line):
                cpu_break = True
                user = re.findall('^CPU\sstates\s+:+\s+(\d.\d+)',line)
                user = float(user[0])
                kernel =re.findall('^CPU\sstates\s+:+\s+\d.\d+%\suser,\s+(\d.\d+)',line)
                kernel =float(kernel[0])
                
                process = float(user) + float(kernel)
                total = float(user) + float(kernel)
                interrupt = '0'
                #cpu status
                if total<21 :
                    status='Low'
                elif total<81 :
                    status='Medium'
                else:
                    status='High'
                total=str(total)
                
                #cpu interrupt
                

            #break loop
            if cpu_break == True and re.findall('.*#',line):
                break
        #print('\ncpu total :', total)
        ##print('\ncpu total :', total)
        #print('\ncpu status :', status)
        
        memory_break = False
        for line in read_file_list:
            #MEMORY
            #Memory Total
            if re.findall('^Memory usage:\s+(\d+)',line):
                memory_break = True
                memory_total = re.findall('^Memory usage:\s+(\d+)',line)
                memory_total = memory_total[0]
                
            #Memory Used
            if re.findall('^Memory usage:\s+\d+.*total,\s+(\d+)',line):
                memory_used = re.findall('^Memory usage:\s+\d+.*total,\s+(\d+)',line)
                memory_used = memory_used[0]
               
                #memory percentage
                memory_percentage = (int(memory_used)/int(memory_total))*100
                #memory status
                if float(memory_percentage)<21 :
                    memory_status='Low'
                elif float(memory_percentage)<81 :
                    memory_status='Medium'
                else:
                    memory_status='High'
                memory_percentage=re.findall('(^.{5})*',str(memory_percentage))
                utils=memory_percentage[0]
                
            #break loop
            if memory_break == True and re.findall('.*#',line):
                break
        
        #print('\nmemory total : ', memory_total)
        #print('\nmemory used: ', memory_used)
        #print('\nmemory status  :', memory_status )
        #print('\nmemory percen  :', utils)

        #sorting memory
        list_memory = []
        list_memory_sorted = []
        memory_sorted_break = False
        memory_sorted_add_list = False
        for line in read_file_list:
            #make conditional statement to let program start append to list, and get ready to break loop
            if re.findall('^PID\s+MemAlloc\s+MemLimit+\s+StkSize\s+RSSMem\s+LibMem\s+StackBase/Ptr\s+Process',line):
                memory_sorted_break = True
                memory_sorted_add_list = True
            #append value to list
            if memory_sorted_break == True:
                if re.findall('^PID\s+MemAlloc\s+MemLimit+\s+StkSize\s+RSSMem\s+LibMem\s+StackBase/Ptr\s+Process',line):
                    pass
                else:
                    list_memory.append(line)
                    
            #break loop
            if memory_sorted_break == True and re.findall('.*#',line):
                break
            elif memory_sorted_break == True and re.findall('^\s*$',line):
                break
        #create new list that only contain memory allocated and name application that using it
        for i in list_memory:
            try:             
                sort_digit = re.findall('\d+\s+\d+\s+\d+\s+(\d+)\s+\S+\/\S+\s+.*',i)
                sort_text =  re.findall('\d+\s+\d+\s+\d+\s+\d+\s+\S+\/\S+\s+(.*)',i)
                list_memory_sorted.append(sort_digit[0]+' '+sort_text[0])
                
            except:
                pass
        try:
            #sort memory with allocated as key
            list_memory_sorted.sort(reverse=True,key = lambda x: int(x.split()[0]))
            ##print('Memory Top Three')
            topproc1 = re.findall('\d+\s+(.*)',list_memory_sorted[0])
            topproc2 = re.findall('\d+\s+(.*)',list_memory_sorted[1])
            topproc3 = re.findall('\d+\s+(.*)',list_memory_sorted[2])
            topproc = (topproc1[0]+'\n'+topproc2[0]+'\n'+topproc3[0])
            
        except:
            pass
        ##print('\n\nlist memory :',list_memory)
        ##print('\n\nlist memory sorted :',list_memory_sorted)    
        #print('\n\nmemory top 3: ', topproc)

        #sorting cpu
        list_cpu = []
        list_cpu_sorted = []
        cpu_sorted_break = False
        cpu_sorted_add_list = False
        for line in read_file_list:
            #make conditional statement to let program start append to list, and get ready to break loop
            if re.findall('.*PID\s+Runtime\S+\s+Invoked\s+uSecs\s+1Sec\s+Process',line):
                cpu_sorted_break = True
                cpu_sorted_add_list = True
            #append value to list
            if cpu_sorted_break == True:
                if re.findall('.*PID\s+Runtime\S+\s+Invoked\s+uSecs\s+1Sec\s+Process',line):
                    pass
                else:
                    list_cpu.append(line)
                    
            #break loop
            if cpu_sorted_break == True and re.findall('.*#',line):
                break
            elif cpu_sorted_break == True and re.findall('^\s*$',line):
                break
        #create new list that only contain cpu allocated and name application that using it
        for i in list_cpu:
            try:
                
                
                sort_digit = re.findall('\d+\s+\d+\s+\d+\s+\d+\s+(\d.\d+)',i)
                sort_text =  re.findall('\d+\s+\d+\s+\d+\s+\d+\s+\d.\d+%\s+(\S*)',i)
                list_cpu_sorted.append(sort_digit[0]+' '+sort_text[0])
                
            except:
                pass
        try:
            #sort cpu with allocated as key
            list_cpu_sorted.sort(reverse=True,key = lambda x: float(x.split()[0]))
            ##print('cpu Top Three')
            topcpu1 = re.findall('\d+\s+(.*)',list_cpu_sorted[0])
            topcpu2 = re.findall('\d+\s+(.*)',list_cpu_sorted[1])
            topcpu3 = re.findall('\d+\s+(.*)',list_cpu_sorted[2])
            topcpu = (topcpu1[0]+'\n'+topcpu2[0]+'\n'+topcpu3[0])
            
        except:
            pass
        ##print('\n\nlist cpu :', list_cpu)
        ##print('\n\nlist cpu sorted:',list_cpu_sorted)
        #print('\n\ncpu top 3', topcpu)


        
        read_file_list_env  = []
        read_file_logic_check = False
        count_read_file = 0
        for line in read_file_list:
            read_file_list_env.append(line)
            if read_file_logic_check == True and 'show' in line:
                break
            if 'show env' in line and '%' not in read_file_list[count_read_file+1] and 'show env' in line and '%' not in read_file_list[count_read_file+1] and '%' not in read_file_list[count_read_file+2] and '!' not in read_file_list[count_read_file+1]:
                read_file_logic_check = True
            count_read_file+=1

        #get environment
        list_psu_capture = []
        list_fan = []
        list_fan_cond_cp = []
        list_temp = []
        list_temp_cond = []
        list_psu = []
        list_psu_cond = []
        psu_line_start = 0
        psu_line_end = 0
        count_line=0
        for i in read_file_list_env:
            if re.findall('^(Fan-.)\s+N3K\S+\s+\S+\s+\S+',i):
                regex_fan = re.findall('^(Fan-.)\s+N3K\S+\s+\S+\s+\S+',i)
                #tulis = input(i)
                fan = regex_fan[0]
                list_fan.append(fan)
                ##print(fan)
            if re.findall('^Fan-.\s+N3K\S+\s+\S+\s+(\S+)', i):
                regex_fan_cond = re.findall('^Fan-.\s+N3K\S+\s+\S+\s+(\S+)', i)
                fan_cond = regex_fan_cond[0]
                list_fan_cond_cp.append(fan_cond)
                ##print(fan_cond)
            #    break
            if re.findall('^\d+\s+(\S+.*)\(\S+\s+\d+\s+\d+\s+\d+\s+\S+',i):
                regex_temp = re.findall('^\d+\s+(\S+.*)\(\S+\s+\d+\s+\d+\s+\d+\s+\S+',i)
                temp = str(regex_temp[0])
                list_temp.append(temp)
            #    break
            if re.findall('^\d+\s+\S+.*\(\S+\s+\d+\s+\d+\s+\d+\s+(\S+)', i):
                regex_temp_cond = re.findall('^\d+\s+\S+.*\(\S+\s+\d+\s+\d+\s+\d+\s+(\S+)', i)
                temp_cond = regex_temp_cond[0]
                list_temp_cond.append(temp_cond)
            #    break
            if re.findall('^(\d+)\s+\S+\s+AC+\s+\d+.\d+\s+\d+.\d+\s+\S+',i):
                regex_psu = re.findall('^(\d+)\s+\S+\s+AC+\s+\d+.\d+\s+\d+.\d+\s+\S+',i)
                psu = regex_psu[0]
                list_psu.append(psu)
            #  break
            if re.findall('^\d+\s+\S+\s+AC+\s+\d+.\d+\s+\d+.\d+\s+(\S+)', i):
                regex_psu_cond = re.findall('^\d+\s+\S+\s+AC+\s+\d+.\d+\s+\d+.\d+\s+(\S+)', i)
                psu_cond = regex_psu_cond[0]
                list_psu_cond.append(psu_cond)
            #break
        ##print('\n\nfan : ',fan)
        #print('\n\nfan : ',list_fan)
        #print('\n\nlist fan kondisi : ', list_fan_cond_cp)
        #print('\n\nlist temperatur : ', list_temp)
        #print('\n\ntemperatur kondisi : ', list_temp_cond)
        #print('\n\nlist psu : ', list_psu)
        #print('\n\nlist psu kondisi : ', list_psu_cond)
        
       #open db connection
        db = sqlite3.connect('pmdb')
        cursor = db.cursor()
        #db software

        cursor.execute('''INSERT INTO swsumtable(version)
                VALUES(?)''', (version,))


        cursor.execute('''INSERT INTO swtable(devicename, model, iosversion, uptime, confreg)
                VALUES(?,?,?,?,?)''', (devicename, model, iosversion, uptime, confreg,))

        #db hardware

        cursor.execute('''INSERT INTO hwsumtable(model)
                VALUES(?)''', (model,))
        count_sql = 0


        for card in list_card:
                cursor.execute('''INSERT INTO hwcardtable(devicename, model, card, sn, hwdscr)
                        VALUES(?,?,?,?,?)''', (devicename,model,card,list_serial_number[count_sql],list_hardware_description[count_sql],))    
                count_sql+=1

        #db process cpu and memory

        cursor.execute('''INSERT INTO cpusumtable(devicename, model, total, process, interrupt, topcpu, status)
                VALUES(?,?,?,?,?,?,?)''', (devicename, model, total, process, interrupt, topcpu, status,))
          

        cursor.execute('''INSERT INTO memsumtable(devicename, model, utils, topproc, status)
                VALUES(?,?,?,?,?)''', (devicename, model, utils, topproc, status,))

        #db environment

        count_sql = 0
        for psu in list_psu:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                    VALUES(?,?,?,?)''', (devicename,'Power Supply',psu,list_psu_cond[count_sql],))
            count_sql+=1


        count_sql = 0
        for fan in list_fan:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                    VALUES(?,?,?,?)''', (devicename,'Fan',fan,list_fan_cond_cp[count_sql],))
            count_sql+=1


        count_sql = 0
        for temp in list_temp:
            cursor.execute('''INSERT INTO envtable(devicename, system, item, status)
                    VALUES(?,?,?,?)''', (devicename,'Temperature',temp,list_temp_cond[count_sql],))
            count_sql+=1

       #LOG Checking

        cursor.execute('''INSERT INTO logtable(devicename, model, script)
                VALUES(?,?,?)''', (devicename, model,self.__class__.__name__,))

        db.commit()             
        db.close()