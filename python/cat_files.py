def catter(virus_parts, infiles):
    v_p = list(virus_parts)
    ins = list(infiles)
    in_v_p = [f.split('/')[1].split('.')[0] for f in ins]

    print(v_p, '\n', in_v_p)

    '''
    example: data/GLRaV3_55_KDa_protein.fasta
    need to find a convenient way to cat all the stuff 
    '''
 
    for f in ins:  
