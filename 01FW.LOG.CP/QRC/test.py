def write_to_sheets(R, List, Sheet_Name):
    for Colum in range(len(List)):
        Sheet_Name.write(R, Colum, List[Colum])


    subnet_list = ["10.2.0.0/16",
               "10.11.0.0/16",
               "10.12.0.0/16",
               "192.168.2.0/24",
               "192.168.100.0/24",
               "192.168.200.0/24",
                   "0.0.0.0/0"]
    open_permit_csv_path = open(permit_csv_path, 'r')
    all_permit_lines = open_permit_csv_path.readlines()
    permit_excel = xlwt.Workbook(encoding='utf-8')

    for subnet01 in subnet_list:
        for subnet02 in subnet_list:
            if (subnet01 != subnet02):
                RuleList = []
                Count = 0
                for eachline in all_permit_lines:
                    if (Count == 0):
                        Title = eachline.split(",")
                        Count += 1
                    else:
                        eachlist = eachline.split(",")
                        Src_IP = eachlist[2]  # Src IP
                        Dst_IP = eachlist[3]  # Dst IP
                        if (Src_IP in IPy.IP(subnet01) and Dst_IP in IPy.IP(subnet02)):
                            RuleList.append(eachlist)
                            Count += 1
                if (RuleList):
                    SheetName = subnet01.split("/")[0] + " to " + subnet02.split("/")[0]
                    SheetName = str(SheetName)
                    mysheet = permit_excel.add_sheet(SheetName)
                    write_to_sheets(0, Title, mysheet)
                    for i in range(len(RuleList)):
                        write_to_sheets(i + 1, RuleList[i], mysheet)
    OtherList = []
    Flag = 0
    for eachline in all_permit_lines:
        if (Flag == 0):
            Flag += 1
        else:
            eachlist = eachline.split(",")
            flag01 = 0
            flag02 = 0
            Src_IP = eachlist[2]  # Src IP
            Dst_IP = eachlist[3]  # Dst IP
            for SubNet in subnet_list:
                if (Src_IP in IPy.IP(SubNet)):
                    flag01 = 1
                if (Dst_IP in IPy.IP(SubNet)):
                    flag02 = 1
            if (flag01 == 0 or flag02 == 0):
                OtherList.append(eachlist)
    Other_SheetName = "Others"
    Other_sheet = permit_excel.add_sheet(Other_SheetName)
    write_to_sheets(0, Title, Other_sheet)
    for i in range(len(OtherList)):
        write_to_sheets(i + 1, OtherList[i], Other_sheet)
    permit_excel.save(permit_rule_exl_path)

    timestamp5 = time.clock()