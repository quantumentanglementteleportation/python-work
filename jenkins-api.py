# https://medium.com/@prashant.vats/trigger-jenkins-job-remotely-using-python-22420792bac2

import jenkins, json, sys


def get_server_instance():
    j_url = 'http://localhost:8080'
    server = jenkins.Jenkins(j_url, username='sumit', password='redhat')
    return server

class ReadJson:
    def __init__(self):
        json_file = sys.argv[1]
        self.build_params_key = []
        self.build_params_value = []
        print("User provided file: %s" %json_file)
        
        with open(json_file) as f:
            data = json.load(f)
            for job in data['job_info']:
                self.user_job = job['name']
                self.param_dict = job['parameters']
                for p in self.param_dict:
                    for key, value in p.items():
                        self.build_params_key.append(key)
                        self.build_params_value.append(value)


class JobDetails:
    def __init__(self):
        call_readjson = ReadJson()
        self.user_job_name = call_readjson.user_job
        user_build_param_list = call_readjson.build_params_key
        self.user_prama_key_value = call_readjson.param_dict

        job_param_list = []
        server = get_server_instance()
        for j in server.get_all_jobs(folder_depth=None):
            if self.user_job_name in j['fullname']:
                job_info = server.get_job_info(self.user_job_name)
                #print(json.dumps(job_info, indent=4, sort_keys=True))

                # Get job parameters
                for get_param in job_info['actions'][0]['parameterDefinitions']:
                    #print(get_param['name'])
                    job_param_list.append(get_param['name'])
                
                total_params_in_job = len(job_param_list)
                total_user_provided_param = len(user_build_param_list)

                if total_params_in_job != total_user_provided_param:
                    raise Exception("User provided params count is not matching with job params")
                
                # Validate User provide params with "job_param_list"
                for user_prama_name in user_build_param_list:
                    if user_prama_name not in job_param_list:
                        raise Exception('%s is not in build required params list' %user_prama_name)

            
            #print(job_param_list)
            #print(json.dumps(job_info['actions'][0]['parameterDefinitions'][0]['name'], indent=4, sort_keys=True))

            # Get last successful build info
            #if job_info['lastSuccessfulBuild'] is not None:
            #    last_build_number = job_info['lastSuccessfulBuild']['number']
            #    last_build_info = json.dumps(server.get_build_info(
            #        read_job, last_build_number), indent=4, sort_keys=True)
            #    print(last_build_info)
#
            #print('Next build Number: ', job_info['nextBuildNumber'])
                self.next_build_num = job_info['nextBuildNumber']
            else:
                print('no matching job')

if __name__ == "__main__":
    check_job = JobDetails()
    print('Starting build for job: %s' % check_job.user_job_name)
    print('Build parameters:')
    for prama_key_value in check_job.user_prama_key_value:
        for key, value in prama_key_value.items():
            print('\t %s: %s' % (key, value))
    #print(check_job.user_prama_key_value[0])

    build_confirmation = input('Continue? "y/n": ')

    if 'y' in build_confirmation or 'yes' in build_confirmation or 'Y' in build_confirmation:
        print('Starting build....')
        server = get_server_instance()
        output = server.build_job(check_job.user_job_name, check_job.user_prama_key_value[0])
        from time import sleep; sleep(10)
        print(json.dumps(server.get_build_info(check_job.user_job_name, output), indent=4, sort_keys=True))
    elif 'n' in build_confirmation or 'N' in build_confirmation or 'no' in build_confirmation:
        print('Exit...')
    else:
        raise Exception('Error: Invalid input!')
