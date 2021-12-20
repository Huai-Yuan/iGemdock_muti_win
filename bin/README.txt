=====================================================================
Installation of iGEMDOCK
=====================================================================

This document is quick installation guide for iGEMDOCK. 

For more information, please visit our web site
http://gemdock.life.nctu.edu.tw/dock/igemdock.php

To update iGEMDOCK and download user guide, please visit our web site at 
http://gemdock.life.nctu.edu.tw/dock/download.php

If you have any problems for iGEMDOCK, please feel free to contact us
http://gemdock.life.nctu.edu.tw/bioxgem/contactus.php

=====================================================================
For Windows users
=====================================================================

Download iGEMDOCK to your desktop

1. Decompress the iGEMDOCKv2.1.zip
2. execute the iGemdock.exe in the folder "bin"


=====================================================================
For Linux users
=====================================================================

Download iGEMDOCK (e.g., iGEMDOCKv2.1-centos.tar) to your desktop. For example, download to the directory "/home/user/Desktop"

1. Change directory to your Desktop and decompress the tar file
Example command:
>cd /home/user/Desktop
>tar -xf ./iGEMDOCKv2.1-centos.tar

2. Change to the sub-folder "bin". The folder is located in the folder of iGEMDOCK.

3. Change the authority to "755" for the files in the "bin" folder.
Example command:
>cd ./iGEMDOCKv2.1-centos/bin
>chmod 755 *

4. Start iGEMDOCK (by executing iGemdock or using iGemdock.sh)

4.1. Start iGEMDOCK by executing "iGemdock" (If you have installed Qt library)
>./iGemdock

4.2. Start iGEMDOCK by executing "iGemdock.sh" or by following commands (If you do not install Qt library)
Example command: (Start from iGemdock.sh)
>./iGemdock.sh
or >bash iGemdock.sh

4.3. Manually setup library and start iGemdock (If you do not use bash and not install Qt library)
>LD_LIBRARY_PATH=/home/user/Desktop/iGemdockv2.1-centos/bin
>export LD_LIBRARY_PATH
>./iGemdock
