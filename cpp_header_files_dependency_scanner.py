import os
import sys
import re

def collect_source_files(source_root_dir, sub_destination_dir, dependences):
    scan_dir = os.path.join( source_root_dir, sub_destination_dir )
    if not os.path.isdir(scan_dir):  
        print( "%s is not a directory" % scan_dir )
        exit(-1)

    for root, sub_dirs, files in os.walk(scan_dir):
        for special_file in files:
            if special_file.endswith(".cpp") : 
                its_deps = {}
                full_source_file_name = os.path.join(sub_destination_dir, special_file)
                dependences[full_source_file_name] = its_deps 
                output( full_source_file_name, 0 )
        for sub_dir in sub_dirs:
            sub_dest_dir = os.path.join( sub_destination_dir, sub_dir )
            print "current dir : %s, sub_dir : %s, sub_dest_dir: %s " % ( sub_destination_dir, sub_dir, sub_dest_dir )
            collect_source_files( source_root_dir, sub_dest_dir, dependences )

def output( msg, indent ):
    print "%s%s" % ( "\t"*indent, msg )
    f = open("simulate.deps.anaysis.txt", "a")
    f.write("%s%s\n" % ( "\t"*indent, msg ))
    f.close()

def scan_dependences( source_root_dir, source_file_name, sub_destination_dir, its_deps, indent ):
    full_source_file_name = os.path.join( source_root_dir, sub_destination_dir, source_file_name )
    if not os.path.isfile(full_source_file_name):
        #print "%s, is not a file in %s, will search without %s " % ( full_source_file_name, source_root_dir, sub_destination_dir )
        full_source_file_name = os.path.join( source_root_dir, source_file_name )
        if not os.path.isfile(full_source_file_name):
            #print "%s, is not a file in %s, ingored" % ( full_source_file_name, source_root_dir )
            return 

    #output( source_file_name, indent )         
    source_file = open(full_source_file_name)     
    line = source_file.readline()
    while line:
        line_str = line.strip() 
        rel = re.search('\#include ".*h"', line_str)
        if rel: 
            begin = line_str.find('"')
            end = line_str.rfind('"')
            h_file_name = line_str[begin+1:end]
            output( h_file_name, indent+1 )         
            h_des_dir = ""
            end = h_file_name.rfind('/')
            if end != -1 : 
                h_des_dir = h_file_name[:end]
                h_file_name = h_file_name[end+1:]
            else:
                end = source_file_name.rfind('/')
                if end != -1 : 
                    h_des_dir = source_file_name[:end]
                else:
                    h_des_dir = sub_destination_dir
            if its_deps.has_key(h_file_name): 
                its_deps[h_file_name] = its_deps[h_file_name] + 1 
            else:
                its_deps[h_file_name] = 1 
                scan_dependences( source_root_dir, h_file_name, h_des_dir, its_deps, indent+1 )
        line = source_file.readline()
    source_file.close()

#    for current_dep in current_deps.keys(): 
#        scan_dependences( source_root_dir, current_dep, current_deps[current_dep], its_deps, indent+1 )

def print_dependences( dependences ):
    for source_file in dependences.keys():
        print source_file
        its_deps = dependences[source_file]
        for dep in its_deps.keys():
            print "  %s, %d " % ( dep, its_deps[dep] )

if __name__ == "__main__":
    print("scan begin")
    dependences = {}
    source_root_dir = str(sys.argv[1])
    sub_destination_dir = str(sys.argv[2])
    print "collecting source files under %s " % sub_destination_dir 
    collect_source_files(source_root_dir, sub_destination_dir, dependences)
    print "Done: collecting source files under %s " % sub_destination_dir 
    print "scan dir: %s under %s " % ( sub_destination_dir, source_root_dir )
    for source_file_name in dependences.keys(): 
        its_deps = dependences[source_file_name]
        output( source_file_name, 0 )
        scan_dependences( source_root_dir, source_file_name, "", its_deps, 0)
    print("scan done")
    print_dependences( dependences )
