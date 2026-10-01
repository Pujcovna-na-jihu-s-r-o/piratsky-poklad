# Pirátský poklad – appka na iPhone (OTA, stejně jako Nežer)

Appka je Capacitor (web v nativním obalu). Publikuje se **přes vzduch (OTA)**,
stejně jako Nežer: GitHub Actions na macOS postaví **podepsanou `.ipa`**, vyrobí
instalační stránku s odkazem `itms-services://` a nahraje to na server. Na iPhonu
se instaluje **odkazem v Safari**, bez Macu a bez Sideloadly, platí rok (Ad Hoc).

- **Podpis:** týmový distribuční certifikát „Pujcovna na jihu s.r.o." + Ad Hoc
  wildcard profil **Kukacka Wildcard AdHoc** (`cz.kukacka.*`). Bundle id appky je
  `cz.kukacka.piratskypoklad`, spadá pod wildcard, takže se nezakládá nový App ID.
- **Zvuky** se tahají zvlášť z `https://www.kukackovi.cz/piratsky-poklad/audio/`
  (nejsou v balíčku), appka si je stáhne za běhu do úložiště.
- **Instalační stránka + .ipa** jsou na `https://www.kukackovi.cz/piratsky-poklad/app/`.

## Jednorázové nastavení

### 1) Server (kukackovi.cz, přes FTP)
- Nahraj `server/ota.php` jako `/piratsky-poklad/ota.php`.
- Vedle něj vytvoř `/piratsky-poklad/ota-token.txt` s jedním dlouhým náhodným
  řetězcem (to je push token).
- Složka `/piratsky-poklad/app/` se vytvoří sama při prvním nahrání.

### 2) Ad Hoc profil se všemi zařízeními
Aby hra šla na všechny rodinné iPhony, musí být v profilu jejich zařízení.
V Apple Developer → Profiles → **Kukacka Wildcard AdHoc** → Edit → zaškrtni
**všechna zařízení** → Save → **Download**. Stažený `.mobileprovision` převeď na
base64 a dej do secretu `IOS_PROVISION_PROFILE` (viz níže).
(Nová zařízení přidaná později = profil znovu vygenerovat a secret aktualizovat.)

### 3) GitHub secrets (repo Pujcovna-na-jihu-s-r-o/piratsky-poklad → Settings → Secrets → Actions)
| secret | hodnota |
|---|---|
| `IOS_CERT_P12_BASE64` | týmový distribuční `.p12` v base64 (stejné jako u Nežera/Faktur) |
| `IOS_CERT_PASSWORD` | heslo k tomu `.p12` |
| `IOS_PROVISION_PROFILE` | base64 profilu „Kukacka Wildcard AdHoc" |
| `PP_WEB_URL` | `https://www.kukackovi.cz/piratsky-poklad` |
| `PP_PUSH_TOKEN` | stejný token jako v `ota-token.txt` |

Base64 na Windows (PowerShell):
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("cesta\k\profilu.mobileprovision")) | Set-Clipboard
```

## Build a instalace
1. Push do `main` (nebo Actions → *iOS OTA* → Run workflow) spustí build.
2. Workflow podepíše `.ipa`, nahraje ji + stránku na server a ověří.
3. Na iPhonu otevři v **Safari**: `https://www.kukackovi.cz/piratsky-poklad/app/`
   → **Nainstalovat**. Potvrď důvěru v Nastavení → Obecné → VPN a správa zařízení.
4. Při prvním spuštění appka stáhne hlasy (jen poprvé), pak jede offline.

## Když se hra změní
Uprav `app/www/` a pushni – workflow postaví a nasadí novou verzi. Platnost
instalace je rok (Ad Hoc); do té doby stačí znovu otevřít instalační odkaz.

## Co je uvnitř
- `app/www/` – hra: `index.html` + `fonts/` (offline); zvuky se stahují ze serveru.
- `.github/workflows/ios-ota.yml` – build podepsané .ipa a nasazení na server.
- `server/ota.php` – přijímač balíčku na server (push token, pevný seznam souborů).
- `app/assets/` – ikona a splash.
