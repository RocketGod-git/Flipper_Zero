# Payload Library for O.MG Devices

This repository contains payloads and extensions for O.MG Devices. Community developed payloads are listed and developers are encouraged to create pull requests to make changes to or submit new payloads.

## About the O.MG Cable


To get a cable like this, you used to need a million dollar budget or to find a guy named MG at DEFCON. But Hak5 teamed up with MG to allow more people access to this previously clandestine attack hardware.

-   [Purchase at Hak5](https://shop.hak5.org/collections/mischief-gadgets/)
-   [Documentation](https://github.com/O-MG/O.MG_Cable-Firmware/wiki)
-   [Discord](https://hak5.org/discord) (Join #omg-support)

![OMG Cable](https://cdn.shopify.com/s/files/1/0068/2142/files/omg_400x.png?v=1604676891)

## Documentation
Documentation on developing payloads for the OMG Cable can be found on the [OMG Wiki](https://github.com/O-MG/O.MG_Cable-Firmware/wiki).

## Disclaimer
Generally, payloads may execute commands on your device or target. As such, it is possible for a payload to damage your device or target. Payloads from this repository are provided AS-IS without warranty. While Hak5 makes a best effort to review payloads, there are no guarantees as to their effectiveness. As with any script, you are advised to proceed with caution.

## Legal
Payloads from this repository are provided for educational purposes only.  Hak5 gear is intended for authorized auditing and security analysis purposes only where permitted subject to local and international laws where applicable. Users are solely responsible for compliance with all laws of their locality. Hak5 LLC and affiliates claim no responsibility for unauthorized or unlawful use.

## Contributing
Once you have developed your payload, you are encouraged to contribute to this repository by submitting a Pull Request. Reviewed and Approved pull requests will add your payload to this repository, where they may be publically available.

Please adhere to the following best practices and style guide when submitting a payload.

### Naming Conventions
Please give your payload a unique and descriptive name. Do not use spaces in payload names. Each payload should be submit into its own directory, with `-` or `_` used in place of spaces, to one of the categories such as exfiltration, phishing, remote_access or recon. Do not create your own category.

### Comments
Payloads should begin with comments specifying at the very least the name of the payload and author. Additional information such as a brief description, the target, any dependencies / prerequisites and the LED status used is helpful.

    REM Title: FTP Exfiltrator
    REM Description: Exfiltrates files from %userprofile%\documents via FTP
    REM Author: Hak5Darren
    REM Target: Windows XP SP3 - Latest
   
