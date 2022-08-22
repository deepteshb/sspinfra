node('vmnode'){

    properties([parameters([ 
        string(defaultValue: '1', name: 'id'), 
        string(defaultValue: '1', name: 'requestid'),
        string(defaultValue: '1', name: 'customer'),
        string(defaultValue: '1', name: 'product'),
        string(defaultValue: '1', name: 'version'),
        string(defaultValue: '1', name: 'component'),
        string(defaultValue: '1', name: 'instances'),
        string(defaultValue: '"ToBeChanged"', name: 'datastore'),
        ])])

    WORKSPACE = params.requestid
    WORK_DIR = params.id+'_'+params.product+'_'+params.version+'_'+params.component
    dir(WORKSPACE){
       stage('CREATE WORKSPACE'){
           dir(WORK_DIR){

               stage('CHECKOUT'){
                   
                   //git(url: 'https://github.com/deepteshb/sspinfratfmodules.git', branch: 'main' )
                   //p4sync charset: 'none', credential: '88fc40cb-c21e-41d4-9c04-a92ed6f3f1b9', format: 'jenkins-${JOB_NAME}', populate: autoClean(delete: true, modtime: false, parallel: [enable: false, minbytes: '1024', minfiles: '1', threads: '4'], pin: '', quiet: true, replace: true, tidy: false), source: depotSource('Add a Source')
                   powershell '''
                   $currentlocation = Get-Location
                   Write-Host $currentlocation
                   Set-Location $currentlocation
                   $destination = Get-Location
                   Write-Host $destination
                   
                   Copy-Item -Path "C:\\Users\\IndiaAdmin\\template.tf" -Destination "$destination\\template.tf" -Recurse -Force
                   '''
               }
                stage('GENERATE'){
                        powershell '''
                        $filePath = '.\\template.tf'
                        $newfile = '.\\main.tf'
                        $variable1 = '"'+$($env:customer)+$($env:product)+'"'
                        $find = 'var.vapp_name'
                        $replace = $variable1
                        (Get-Content -Path $filePath) -replace $find, $replace | Set-Content -Path $newfile  -Force
                        $filePath = '.\\main.tf'
                        $newfile = '.\\main.tf'
                        $variable2 = '"'+ $($env:component) +'"'
                        $find = 'var.templatename'
                        $replace = $variable2
                        (Get-Content -Path $filePath) -replace $find, $replace | Set-Content -Path $newfile  -Force
                        $filePath = '.\\main.tf'
                        $newfile = '.\\main.tf'
                        $variable3 = '"'+$($env:customer)+$($env:product)+'_'+$($env:version)+'_${count.index}"'
                        $find = 'var.vm_name'
                        $replace = $variable3
                        (Get-Content -Path $filePath) -replace $find, $replace | Set-Content -Path $newfile  -Force
                        $newfile = '.\\main.tf'
                        $variable4 = $($env:instances)
                        $find = '"countofmachines"'
                        $replace = $variable4
                        (Get-Content -Path $filePath) -replace $find, $replace | Set-Content -Path $newfile  -Force
                        Remove-Item ./template.tf
                        '''
                                }

                stage('INITIALIZE'){
                    powershell '$env:Path'
                    powershell 'echo "terraform will initialise"'
                    powershell label: 'TFVERSION', returnStdout: true, script: 'C:\\terraform\\terraform.exe --version' 
                    powershell label: 'TFINIT', returnStdout: true, script: 'C:\\terraform\\terraform.exe init'
                }

                stage('PLAN'){
                    powershell 'echo "This is the terraform plan stage"'
                    powershell label: 'TFPLAN', script: 'C:\\terraform\\terraform.exe plan'
                    
                }
                
                stage('QUEUED'){
                                powershell '''
                                $env:PGPASSWORD = 'abc123'
                                $requestid = $($env:requestid)
                                echo $requestid
                                E:\\Postgres\\bin\\psql.exe -U postgres -d sspinfra_dev -c "update launchrequests set status ='QUEUED' where request_id = $requestid"
                                ''' 
                }

                stage('LAUNCH'){
                    powershell label: 'TFAPPLY', script: 'C:\\terraform\\terraform.exe apply -auto-approve'
                    
            }

            stage('GET IP'){
                   def msg = powershell(returnStdout: true, script: 'C:\\terraform\\terraform.exe output')
                   echo "defining the msg variable"
                   echo msg
                   def emailBody = ''' 
                    <html>
                        <body>
                            <h1> Machine Details</h1>
                            <p> Hi, you have requested to provision the following machines </p>
                            <p> The IP Address for the machines are: </p>
                        </body>
                    </html>         
            '''
            echo "Adding subject and  executing email task"
            def emailSubject = "SSPINFRA-INFRA PROVISIONING STATUS AND REPORT - Build Status"
            def machines = params.customer + params.product + params.version
            echo machines
            emailext(mimeType: 'text/html', replyTo: '', subject: emailSubject, to: "", body: emailBody + machines + msg )
            //emailext attachLog: true, body: msg, subject: 'VM is successfully launched', to: ''
            echo "email has been successfully sent"
            echo "executing powershell for entering records in DB"
            powershell '''
            $env:PGPASSWORD = 'abc123'
            $requestid = $($env:requestid)
            echo $requestid
            E:\\Postgres\\bin\\psql.exe -U postgres -d sspinfra_dev -c "update launchrequests set status ='PROVISIONED' where request_id = $requestid"
            ''' 
            }
            
            

       }
      
    }


}
}