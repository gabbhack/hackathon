select User {id, token := <str>$token} filter .tokens.value = <str>$token limit 1