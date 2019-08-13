import json
from collections import Counter 


def json_to_fasta(infile, outfile, viruses):
    print('input', infile)

    out_f_list = list(outfile)
    files = [str(inf) for inf in infile]
    viruses = list(viruses)

    # print(files, viruses)

    

    def flatten(lst):
        new_lst = [i for l in lst for i in l]
        return new_lst

    def name_fixer(count):
        temp = count.replace(' ', '_')
        t_t = temp.replace(',', '__')
        name = t_t.replace('/','__')
        return name

    for pos, virus in enumerate(viruses):

        master_dict = {'GVA': ('Grapevine virus A', 'Grapevine virus A (GVA)'),\
                        'GLRaV3' :('Grapevine leafroll-associated virus 3 (GLRaV-3)','Grapevine leafroll-associated virus 3m'),\
                         'GPGV' :('Grapevine Pinot gris virus','Grapevine Pinot gris virus')} 

        search_term = master_dict[virus]

        acc_num = []
        products = []
        source = []
        country = []
        seq = []
        host = []
        date = []
        pro_id = []
        trans = []
        file = files[pos]
        with open(file) as in_f:
            data = json.load(in_f)
            for p in data.items():
                virus_source = p[1]['source'][0]
                if virus_source == search_term[0] or virus_source == search_term[1]:
                    acc_num.append(p[0])
                    products.append(p[1]['product'])
                    source.append(p[1]['source'])
                    country.append(p[1]['country'])
                    seq.append(p[1]['seq'])
                    host.append(p[1]['host'])
                    date.append(p[1]['date'])
                    pro_id.append(p[1]['pro_id'])
                    trans.append(p[1]['trans'])

        # print(len(acc_num), len(products), len(seq))
        if len(acc_num) == len(products) == len(seq):
            term = "There were %d sequences found for %s!" % (len(acc_num), virus)
            print(term)

        
        flat_products = flatten(products)
        source = flatten(source)
        counted_prods = list(Counter(flat_products))
        counted_source = Counter(source)

        zipped = list(zip(acc_num, products, pro_id, trans, country, seq, host, date))
        
        '''
        order
        name, seq_acc_num, place, hst, time, pr_id, trs
        '''
        this = []
        for line in zipped:
            if len(line[1]) > 1:
                temp_prods = line[1]
                temp_id = line[2]
                temp_trans = line[3]
                for pos, item in enumerate(temp_prods):
                    
                    name = str(name_fixer(item))
                    acc = str(line[0])
                    p = str(line[4][0])
                    h = str(line[6][0])
                    d = str(line[7][0])

                    test = [name, acc, p, h, d, temp_id[pos], temp_trans[pos]]
                    this.append(test)
                    
            else:
                name = str(name_fixer(line[1][0]))
                acc = str(line[0])
                p = str(line[4][0])
                h = str(line[6][0])
                d = str(line[7][0])
                pr_id = line[2][0]
                trs = line[3][0]
                test = [name, acc, p, h, d, pr_id, trs]
                this.append(test)

        temp_this = [i[0] for i in this]
        count_this = list(Counter(temp_this))

        # print('this ', len(this))
        # print('temp this ', len(temp_this))
        # print('count this', len(count_this))
        # print('counted_prods', len(counted_prods))

        for count in counted_prods:
            print('finding... ', count)
            temp_name = name_fixer(count)
            file_guts = "data/%s_%s.fasta" % (virus, temp_name)
            with open(file_guts, 'w') as out:
                for line in this:
                    this_name = line[0]
                    # print(temp_name, this_name)
                    if temp_name == this_name:
                            p_id = line[5]
                            acc_num = line[1]
                            place = line[2].replace(' ', '-')
                            trans_seq = line[6]
                            host = line[3].replace(' ', '-')
                            date = line[4].replace(' ', '-')
                            header = '%s_%s_%s_%s_%s_%s_' % (p_id, this_name, acc_num, place, date, host)
                            out.write(">{}\n{}\n".format(header, trans_seq))









