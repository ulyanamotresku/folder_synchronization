import hashlib
import os
import time
import shutil
import argparse
import logging


def sync_folders(source, replica, log_file, time_interval):
    source = os.path.abspath(source)
    replica = os.path.abspath(replica)
    
    if not os.path.isdir(replica):
        os.makedirs(replica)

    if not os.path.isdir(source):
        raise argparse.ArgumentError(None, "The source folder doesn't exist.")

    logging.info(f"Start with parameters:\nsource:{source}\nreplica:{replica}\nlog:{log_file}\ntime_interval:{time_interval}\n")

    while True:
        try:
            compare_folders(source, replica)
            time.sleep(time_interval)
        except KeyboardInterrupt:
            print("The Program is terminated manually!")
            raise SystemExit


def compare_files(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()


def compare_folders(source_f, replica_f):
    
    logging.info("----------Starting synchronization...")
    print("----------Starting synchronization...")
    
    files_source = {}
    files_replica = {}
    
    for (dir_path, dir_names, file_names) in os.walk(source_f):
        files_source[dir_path.replace(source_f+'\\', '')]= file_names
    
    for (dir_path, dir_names, file_names) in os.walk(replica_f):
        files_replica[dir_path.replace(replica_f+'\\', '')]= file_names

    for key in files_source:
        if key==source_f:
            for file in files_source[key]:
                
                source_file_path = os.path.join(source_f, file)
                replica_file_path = os.path.join(replica_f, file)
                
                if file in files_replica[replica_f]:
                    if compare_files(source_file_path, replica_file_path):
                        log_message = f"{file} is up to date."
                        logging.info(log_message)
                        print(log_message)
                    else:
                        os.remove(replica_file_path)
                        shutil.copy2(source_file_path, replica_file_path)
                        log_message = f"{file} has been updated."
                        logging.info(log_message)
                        print(log_message)
                else:
                    shutil.copy2(source_file_path, replica_file_path)
                    log_message = f"{file} has been copied."
                    logging.info(log_message)
                    print(log_message)
                    
                        
        if key in list(files_replica.keys()):
            for file in files_source[key]:
                
                source_file_path = os.path.join(source_f, key, file)
                replica_file_path = os.path.join(replica_f, key, file)
                
                if file in files_replica[key]:
                    if compare_files(source_file_path, replica_file_path):
                        log_message = f"{file} is up to date."
                        logging.info(log_message)
                        print(log_message)
                    else:
                        os.remove(replica_file_path)
                        shutil.copy2(source_file_path, replica_file_path)
                        log_message = f"{file} has been updated."
                        logging.info(log_message)
                        print(log_message)
                else:
                    shutil.copy2(source_file_path, replica_file_path)
                    log_message = f"{file} has been copied."
                    logging.info(log_message)
                    print(log_message)
                    
            
        if key not in list(files_replica.keys()) and key!=source_f:
            os.makedirs(os.path.join(replica_f, key))
            log_message = f"{key} folder has been created."
            logging.info(log_message)
            print(log_message)
            for file in files_source[key]:
                
                source_file_path = os.path.join(source_f, key, file)
                replica_file_path = os.path.join(replica_f, key, file)
                
                shutil.copy2(source_file_path, replica_file_path)
                log_message = f"{file} has been copied."
                logging.info(log_message)
                print(log_message)
            
    files_replica = {}
    for (dir_path, dir_names, file_names) in os.walk(replica_f):
        files_replica[dir_path.replace(replica_f+'\\', '')]= file_names
    

    for key in files_replica:
        
        if key==replica_f:
            for file in files_replica[key]:
                
                source_file_path = os.path.join(source_f, file)
                replica_file_path = os.path.join(replica_f, file)
            
                if file not in files_source[source_f]:
                    os.remove(os.path.join(replica_f, file))
                    log_message = f"{file} has been deleted."
                    logging.info(log_message)
                    print(log_message)
                    
                    
        if key in list(files_source.keys()):
            for file in files_replica[key]:
                
                source_file_path = os.path.join(source_f, key, file)
                replica_file_path = os.path.join(replica_f, key, file)
                
                if file not in files_source[key]:
                    os.remove(os.path.join(replica_f, file))
                    log_message = f"{file} has been deleted."
                    logging.info(log_message)
                    print(log_message)
        
        if key not in list(files_source.keys()) and key!=replica_f:
            replica_file_path = os.path.join(replica_f, key)
            try:
                shutil.rmtree(replica_file_path)
                log_message = f"{key} folder has been deleted."
                logging.info(log_message)
                print(log_message)
            except FileNotFoundError:
                log_message = f"{key} folder has already been deleted."
                logging.info(log_message)
                print(log_message)
                return

    logging.info("----------Successful synchronization!")
    print("----------Successful synchronization!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Folder synchronization program')
    parser.add_argument('--source', type=str, default="source", help='Source folder path')
    parser.add_argument('--replica', type=str, default="replica", help='Replica folder path')
    parser.add_argument('--log-file', type=str, default='log.txt', help='Log file path')
    parser.add_argument('--time-interval', type=int, default=60, help='Time interval for synchronization in seconds')
    args = parser.parse_args()

    logging.basicConfig(filename=args.log_file, level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
    sync_folders(args.source, args.replica, args.log_file, args.time_interval)