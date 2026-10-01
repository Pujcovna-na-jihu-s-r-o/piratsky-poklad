# OTA přijímač – Pirátský poklad

`ota.php` přijímá podepsanou appku z GitHub Actions a servíruje instalační stránku.

## Nasazení na kukackovi.cz (FTP)
1. Nahraj `ota.php` jako `/piratsky-poklad/ota.php`.
2. Vedle vytvoř `/piratsky-poklad/ota-token.txt` s jedním dlouhým náhodným
   řetězcem (push token). Stejný token dej do GitHub secretu `PP_PUSH_TOKEN`.
3. Hotovo. Build nahraje balíček do `/piratsky-poklad/app/`.
   Instalace: `https://www.kukackovi.cz/piratsky-poklad/app/` (otevřít v Safari).

## Bezpečnost
- Nahrát jde jen soubory z pevného seznamu (ipa, manifest.plist, build.json,
  index.html, ikony) – žádné `.php`.
- Ověřuje se push token (hash_equals). Token drž mimo repo.
- Přenos po částech kvůli velikosti .ipa; na konci se vrací sha256 ke kontrole.
