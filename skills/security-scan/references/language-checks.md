# Language-Specific Vulnerability Patterns

Apply the section(s) matching the target codebase's languages. Each entry lists a
vulnerability class, dangerous patterns to search for, and the secure alternative.

---

## JavaScript / TypeScript

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| Code injection | `eval()`, `Function()`, `setTimeout(string)`, `setInterval(string)` | Avoid; use `JSON.parse()`, function references |
| XSS (DOM) | `innerHTML`, `outerHTML`, `document.write()`, `insertAdjacentHTML()` | `textContent`, `createElement()`, DOMPurify |
| XSS (React) | `dangerouslySetInnerHTML` | Sanitize with DOMPurify before use |
| Prototype pollution | `Object.assign(target, userInput)`, recursive merge of user objects, `__proto__` | Validate input keys, use `Object.create(null)`, freeze prototypes |
| ReDoS | Complex regex with nested quantifiers on user input: `(a+)+`, `(a|a)*`, `(a+)*` | Use RE2 or safe-regex library; set timeout on regex execution |
| Path traversal | `path.join(base, userInput)` without validation | `path.resolve()` + verify result starts with base directory |
| Insecure randomness | `Math.random()` for tokens/secrets | `crypto.randomBytes()` / `crypto.randomUUID()` |
| Open redirect | `res.redirect(req.query.url)` | Allowlist of valid redirect targets; validate URL host |
| Header injection | User input in `res.setHeader()` | Strip newlines `\r\n` from header values |
| SSRF | `fetch(userUrl)`, `axios.get(userUrl)`, `http.request(userUrl)` | URL allowlist, block private IP ranges, disable redirects |
| Timing attack | String comparison for secrets: `===` | `crypto.timingSafeEqual()` |
| Dependency confusion | Scoped packages without registry lock | Use `.npmrc` with registry pinning, lockfiles |

**Node.js specific:**
- `child_process.exec()` — command injection; use `execFile()` with argument array instead.
- `fs.readFile(userPath)` — path traversal; canonicalize and sandbox.
- `require(userInput)` — arbitrary module loading; never use dynamic require with user input.
- Missing `helmet` or equivalent security headers middleware.
- `express.static` serving sensitive directories.

---

## Python

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| Code injection | `eval()`, `exec()`, `compile()` with user input | Avoid; parse with `ast.literal_eval()` for data only |
| Command injection | `os.system()`, `subprocess.call(shell=True)`, `subprocess.Popen(shell=True)` | `subprocess.run(cmd_list, shell=False)` |
| Deserialization | `pickle.loads(untrusted)`, `yaml.load(untrusted)` (default Loader) | Avoid pickle on untrusted data; use `yaml.safe_load()` |
| SQL injection | f-strings/format/`%` in SQL: `f"SELECT ... WHERE id={user_id}"` | Parameterized queries: `cursor.execute("... WHERE id=%s", (user_id,))` |
| SSTI | `render_template_string(user_input)`, `Template(user_input).render()` | `render_template()` with pre-defined templates only |
| Path traversal | `open(os.path.join(base, user_path))` | `os.path.realpath()` + verify prefix matches allowed directory |
| SSRF | `requests.get(user_url)` | URL allowlist, validate hostname against private ranges |
| Regex DoS | `re.match(user_pattern, data)` | Use `re2` library or timeout; never compile user-supplied patterns |
| Insecure randomness | `random.random()` for secrets | `secrets.token_hex()`, `secrets.token_urlsafe()` |
| XXE | `xml.etree.ElementTree`, `lxml` without disabling entities | `defusedxml` library |
| Jinja2 autoescape | `Environment(autoescape=False)` | `Environment(autoescape=True)` or `select_autoescape()` |
| Django specific | `|safe` filter, `mark_safe()`, `extra()` in ORM, `DEBUG=True` in prod | Minimize `mark_safe`, avoid `extra()`, environment-based settings |
| Flask specific | `app.secret_key = 'hardcoded'`, `debug=True` | Load from environment; never enable debug in production |

---

## Java

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| SQL injection | String concatenation in SQL: `"SELECT ... WHERE id=" + userId` | PreparedStatement with `?` parameters; JPA named parameters |
| Deserialization | `ObjectInputStream.readObject()` on untrusted input | Allowlist via `ObjectInputFilter` (Java 9+), avoid native serialization |
| Command injection | `Runtime.getRuntime().exec(userString)` | `ProcessBuilder` with argument list, input validation |
| XXE | `DocumentBuilderFactory`, `SAXParser`, `XMLReader` default config | Disable external entities: `setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` |
| SSRF | `URL.openStream()`, `HttpURLConnection` with user URL | URL allowlist, hostname validation |
| Log injection | `logger.info("User input: " + userInput)` | Parameterized logging: `logger.info("User input: {}", userInput)` + sanitize newlines |
| Path traversal | `new File(base + userPath)` | `Path.normalize()` + verify `startsWith(allowedBase)` |
| Insecure crypto | `MessageDigest.getInstance("MD5")`, `Cipher.getInstance("DES")` | `MessageDigest.getInstance("SHA-256")`, `Cipher.getInstance("AES/GCM/NoPadding")` |
| EL injection | User input in JSP/JSF EL expressions | Never pass user input to EL evaluation |
| LDAP injection | String concatenation in LDAP filters | Use `javax.naming.ldap.Rdn.escapeValue()` |
| Spring specific | SpEL with user input, disabled CSRF, permissive CORS, actuator endpoints exposed | Never evaluate user input as SpEL; enable CSRF; restrict actuator |
| Log4j | Log4j < 2.17.1 (CVE-2021-44228/45046/45105/44832) | Upgrade to 2.17.1+; set `log4j2.formatMsgNoLookups=true` as interim mitigation |

---

## Go

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| SQL injection | `fmt.Sprintf("SELECT ... WHERE id=%s", userId)` | `db.Query("SELECT ... WHERE id=$1", userId)` |
| Template injection | `template.HTML(userInput)`, `template.JS(userInput)` | Let `html/template` auto-escape; never cast user input to safe types |
| Command injection | `exec.Command("sh", "-c", userString)` | `exec.Command(binary, arg1, arg2)` with separate args |
| Path traversal | `filepath.Join(base, userPath)` without validation | `filepath.Clean()` + verify `strings.HasPrefix(result, base)` |
| SSRF | `http.Get(userURL)` | URL allowlist; custom `http.Transport` with `DialContext` that blocks private IPs |
| Race conditions | Shared state without synchronization, goroutine data races | `sync.Mutex`, channels, `go build -race` for detection |
| Insecure TLS | `InsecureSkipVerify: true` | Remove; use proper CA bundle |
| Error information leak | Returning `err.Error()` to HTTP client | Log internal error; return generic message to client |
| Integer overflow | Unchecked type conversions (e.g., `int64` → `int32`) | Bounds-check before conversion |
| Nil pointer | Missing nil checks on pointers from maps, type assertions | Use comma-ok pattern: `val, ok := m[key]` |

---

## C / C++

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| Buffer overflow | `strcpy`, `strcat`, `sprintf`, `gets`, fixed-size buffers | `strncpy`, `strncat`, `snprintf`, `fgets`; prefer `std::string` in C++ |
| Format string | `printf(userInput)`, `fprintf(f, userInput)` | `printf("%s", userInput)` — always use format specifier |
| Use-after-free | Accessing memory after `free()` | Set pointer to NULL after free; use smart pointers in C++ |
| Integer overflow | Unchecked arithmetic on user-controlled values | Validate ranges; use safe integer libraries |
| Memory leak | Missing `free()` on allocated memory | RAII in C++; static analysis tools (Valgrind, ASan) |
| Command injection | `system(userString)`, `popen(userString)` | `execve()` with argument array |
| Double free | Calling `free()` twice on same pointer | Set pointer to NULL after free |
| Null dereference | Missing null checks on return values | Always check `malloc()`, `fopen()`, etc. return values |
| Uninitialized memory | Using variables before assignment | Initialize all variables; use `-Wuninitialized` |

---

## Ruby

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| Code injection | `eval(user_input)`, `send(user_method)`, `instance_eval` | Avoid; use allowlist of permitted operations |
| Command injection | backticks, `system()`, `exec()`, `%x{}` with user input | `Open3.capture3(cmd, arg1, arg2)` |
| SQL injection | String interpolation in queries: `where("name = '#{params[:name]}'")` | `where(name: params[:name])` or `where("name = ?", params[:name])` |
| Deserialization | `Marshal.load(untrusted)`, `YAML.load(untrusted)` | `YAML.safe_load()`; avoid Marshal on untrusted input |
| Mass assignment | Unpermitted parameters in controllers | `strong_parameters`: `params.require(:user).permit(:name, :email)` |
| XSS | `raw()`, `html_safe` on user input | Let Rails auto-escape; sanitize with `sanitize()` helper |
| Open redirect | `redirect_to(params[:url])` | Allowlist valid paths; use `redirect_to` with only relative paths |
| File access | `File.read(params[:path])` | Validate and canonicalize path; restrict to allowed directory |

---

## PHP

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| Code injection | `eval()`, `assert()`, `preg_replace` with `e` flag | Avoid; use specific functions for the task |
| Command injection | `exec()`, `system()`, `passthru()`, `shell_exec()`, backticks | `escapeshellarg()` + `escapeshellcmd()`, or avoid shell entirely |
| SQL injection | `mysqli_query("... WHERE id=$_GET[id]")` | Prepared statements: `$stmt->bind_param("i", $id)` |
| File inclusion | `include($_GET['page'])`, `require($user_input)` | Allowlist of includable files; never use user input in include |
| Deserialization | `unserialize($_COOKIE['data'])` | `json_decode()` instead; never unserialize user input |
| XSS | `echo $_GET['name']` | `htmlspecialchars($input, ENT_QUOTES, 'UTF-8')` |
| File upload | No type validation, executable uploads | Validate MIME type and extension; store outside webroot; rename files |
| Type juggling | Loose comparison `==` with user input | Use strict comparison `===` |
| SSRF | `file_get_contents($user_url)`, `curl_exec` with user URL | URL allowlist; disable `allow_url_fopen` if not needed |
| XXE | `simplexml_load_string` with external entities enabled | `libxml_disable_entity_loader(true)` (PHP < 8.0) |

---

## C# / .NET

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| SQL injection | `$"SELECT ... WHERE id={userId}"` | `SqlCommand` with `Parameters.AddWithValue()` or Dapper/EF parameterization |
| Deserialization | `BinaryFormatter.Deserialize()`, `JsonConvert.DeserializeObject` with `TypeNameHandling` | Avoid `BinaryFormatter`; set `TypeNameHandling.None` |
| Command injection | `Process.Start("cmd", "/c " + userInput)` | Pass arguments separately; validate input |
| XSS | `@Html.Raw(userInput)` | Default Razor encoding; use `@Html.Encode()` if needed |
| Path traversal | `Path.Combine(base, userPath)` | `Path.GetFullPath()` + verify starts with allowed base |
| XXE | `XmlDocument.Load()` without disabling DTD | Set `XmlReaderSettings.DtdProcessing = DtdProcessing.Prohibit` |
| SSRF | `HttpClient.GetAsync(userUrl)` | URL allowlist; custom `HttpClientHandler` blocking private ranges |
| Cryptography | `MD5.Create()`, `SHA1.Create()`, `DES`, `RijndaelManaged` in ECB | `SHA256`, `Aes` in GCM mode, `HMACSHA256` |
| Regex DoS | `Regex.Match(input, userPattern)` | Set `RegexOptions.MatchTimeout`, validate patterns |

---

## Rust

Rust's ownership model prevents many memory-safety issues, but logic and web vulnerabilities
still apply.

| Vulnerability | Dangerous Pattern | Secure Alternative |
|---|---|---|
| SQL injection | `format!("SELECT ... WHERE id={}", user_id)` in raw SQL | Use `sqlx` query macros with bind parameters |
| Command injection | `Command::new("sh").arg("-c").arg(user_string)` | `Command::new(binary).arg(validated_arg)` |
| Unsafe blocks | Excessive or unnecessary `unsafe {}` | Minimize unsafe; document safety invariants; prefer safe abstractions |
| Panic in production | `unwrap()`, `expect()` on user-controlled input | Use `?` operator, `match`, or `unwrap_or_default()` |
| SSRF | `reqwest::get(user_url)` | URL allowlist; validate hostname |
| Deserialization | `serde_json::from_str::<Value>(untrusted)` with custom deserializers | Strongly typed deserialization; validate input bounds |
| Path traversal | `std::fs::read(user_path)` | Canonicalize path + verify prefix |
