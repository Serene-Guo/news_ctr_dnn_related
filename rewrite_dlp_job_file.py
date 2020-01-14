import os
import argparse



def rewrite_file(source_file, target_file, new_cmd, new_branch):
    
    ### git = ssh://git@g.hz.netease.com:22222/dl/hz-rank-trial.git#generate_train_data_hash_2billion
    f_in = open(source_file, "r")
    f_out = open(target_file, "w")
    has_rewrite_cmd = False
    for line in f_in:
        line = line.strip()
        if len(line) < 1:
            f_out.write(line + "\n")
            continue
        if line[0] == ";" or line[0] == "#":
            f_out.write(line + "\n")
            continue
        if "cmd =" in line or "cmd=" in line:
            if not has_rewrite_cmd:
                f_out.write("cmd = " + new_cmd + "\n")
                has_rewrite_cmd = True
            continue
        if "git =" in line or "git=" in line:
            git_arr = line.split("#")
            new_git_line = git_arr[0] + "#" + new_branch
            f_out.write(new_git_line + "\n")
            continue
        if "name =" in line or "name=" in line:
            len_new_branch = len(new_branch)
            start_index = 0
            if len_new_branch > 25:
                start_index = len_new_branch - 25

            tmp_branch_name = new_branch[start_index:]
            tmp_branch_name = tmp_branch_name.strip("-").strip("_")

            new_name = "name = " + "gff-" + tmp_branch_name.replace('_', '-')
            new_name = new_name.strip("-")
            f_out.write(new_name + "\n")
            continue
        f_out.write(line+"\n")


    f_in.close()
    f_out.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--source_file_name', type=str, required=True)
    parser.add_argument('--new_cmd', type=str, required=True)
    parser.add_argument('--new_branch', type=str, required=True)
    parser.add_argument('--target_file_name', type=str, required=True)

    args, _ = parser.parse_known_args()

    rewrite_file(args.source_file_name, args.target_file_name, args.new_cmd, args.new_branch)
