new_client () {
        # Generates the custom client.ovpn
        {
        cat /etc/openvpn/server/client-common.txt
        echo "<ca>"
        cat /etc/openvpn/server/easy-rsa/pki/ca.crt
        echo "</ca>"
        echo "<cert>"
        sed -ne '/BEGIN CERTIFICATE/,$ p' /etc/openvpn/server/easy-rsa/pki/issued/"$1".crt
        echo "</cert>"
        echo "<key>"
        cat /etc/openvpn/server/easy-rsa/pki/private/"$1".key
        echo "</key>"
        echo "<tls-crypt>"
        sed -ne '/BEGIN OpenVPN Static key/,$ p' /etc/openvpn/server/tc.key
        echo "</tls-crypt>"
        } > ~/ovpn-client-configs/"$1".ovpn
}

cd /etc/openvpn/server/easy-rsa/
./easyrsa --batch --days=3650 build-client-full "$1" nopass
# Generates the custom client.ovpn
new_client
echo
echo "$client added. Configuration available in:" ~/ovpn-client-configs/"$1.ovpn"
exit