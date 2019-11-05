from Bio import SeqIO

def nexus(in_nex):
    in_n = str(in_nex)

    def index_getter(in_n):
        f = open(in_n)
        lines = f.readlines()
        index = []
        trees = []
        for pos, line in enumerate(lines):
            if line.startswith("BEGIN ASSUMPTIONS"):
                index.append(pos+1)
            elif line.startswith("BEGIN TREES"):
                index.append(pos-1)
            elif "TREE tree_" in line:
                trees.append(pos)
            else:
                continue

        splits = list(lines[index[0]: index[-1]])
        good_splits = [t.split(" ")[-1].split(";")[0] for t in splits]

        temp_tree = list(lines[trees[0]: trees[-1]+1])
        good_trees = [t.split(" ")[-1].split(";")[0] for t in temp_tree]
        return good_splits, good_trees

    results = index_getter(in_n)
    inds, trees = results[0], results[1]

    #print(len(trees), len(inds))
    #print(inds)
    files = []
    for pos, i in enumerate(inds):
        prot = in_n.split("/")[-1].split(".hyphy")[0]
        f = "data/fasta/%s.hyphy.fas.GARD.%d.nex" % (prot, pos)
        files.append(f)

    for pos, item in enumerate(files):
        print(f"Writing partition {pos + 1} to {item}")
        with open(item, "w") as out:
            for record in SeqIO.parse(in_n, "nexus"):
                ind_1 = int(inds[pos].split("-")[0]) - 1
                ind_2 = int(inds[pos].split("-")[1])

                r = list(record.seq)
                seq = r[ind_1:ind_2]
                seq = "".join(seq)

                out.write(">{}\n{}\n".format(record.id, seq))


            ## now add the tree to the end of the file ##
            out.write(trees[pos])






