# enum-nosql
MongoDB noSQL injection example from "Hack the Box" for usernames and their password enumeration.

noSQL injection autentication bypass:
If parameter values are directly taken from autentization form as follow:
$query = array("username" => $_POST["username"], "password" => $_POST["password"]);

It's possible to use PHP's associative array processing to inject query that return always true and bypass autentication process.
username[$ne]=""&password[$ne]=""

PHP process malformed input as follow and 
$query = array("username" => array("$ne" => ""), "password" => array("$ne" => ""));

noSQL username and password enumeration:
It's possible to use also regular expressions in query and try to guess username letters one by one.
username[$regex]="^{letter from wordlist}"&password[$ne]=""""

If there is username for example "alice" and we start with first letter from wordlist 'a' with following query:
username="{found username}"&password[$regex]="^a"
the querry returns true so we know that there is username with letter a on first possition. If query returns false we continue with next letter from wordlist. In this way is possible to expose whole username letter by letter. It's necessary to go through all wordlist letters even if query returns true because there could be more usernames specified (alice, alida, allisha,... and of course bob) with same username prefix (in script is possible to solve it with recursions).

after usernames enumeration it's possible to expose also passwords with following querry:
username="{found username}"&password[$regex]="^{letter from wordlist}"

Usage
enum-nosql -u {target_ip}
