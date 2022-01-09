# enum-nosql
MongoDB noSQL injection exploit example from **Hack the Box / mango** <https://app.hackthebox.com/machines/214> for usernames and their password enumeration.

## authentication bypass
If parameter values are directly taken from autentization form as follow:
```php
$query = array("username" => $_POST["username"], "password" => $_POST["password"]);
```

It's possible to use PHP's associative array processing to inject query that return always true and bypass autentication process.
```php
username[$ne]=""&password[$ne]=""
```

PHP process malformed input as follow and 
```php
$query = array("username" => array("$ne" => ""), "password" => array("$ne" => ""));
```

## username and password enumeration
It's possible to use also regular expressions in query and try to guess username letters one by one.
```php
username[$regex]="^{letter from wordlist}"&password[$ne]=""""
```

If there is username for example "alice" and we start with first letter from wordlist 'a' with following query:
```php
username="{found username}"&password[$regex]="^a"
```

The querry returns *true* value so we know that there is username with letter a on first possition. If query returns false we continue with next letter from wordlist. In this way is possible to expose whole username letter by letter. It's necessary to go through all wordlist letters even if query returns true because there could be more usernames specified (alice, alida, allisha,... and of course bob) with same username prefix (in script is possible to solve it with recursions).

After usernames are enumeration it's possible to enumerate passwords with following querry:
```php
username="{found username}"&password[$regex]="^{letter from wordlist}"
```

## usage
```bash
enum-nosql -u {target_ip}
```
