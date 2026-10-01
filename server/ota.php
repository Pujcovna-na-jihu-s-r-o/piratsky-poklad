<?php
/**
 * OTA přijímač balíčku appky „Pirátský poklad" – stejný princip jako u Nežera.
 *
 * GitHub Actions sem nahraje podepsanou .ipa, manifest.plist, instalační stránku,
 * ikony a build.json. Na iPhonu se pak appka instaluje odkazem itms-services
 * z index.html v této složce. Žádné FTP údaje v secrets – nahrává se push tokenem.
 *
 * Nasazení na server (kukackovi.cz):
 *   1) nahraj tenhle soubor jako  /piratsky-poklad/ota.php
 *   2) vedle něj vytvoř soubor    /piratsky-poklad/ota-token.txt  s dlouhým náhodným
 *      tokenem (jeden řádek). Server ho použije k ověření; stejný token dej do
 *      GitHub secretu PP_PUSH_TOKEN.
 *   3) balíček půjde do podsložky  /piratsky-poklad/app/  (vytvoří se sama).
 * Veřejná instalační adresa pak je:  https://www.kukackovi.cz/piratsky-poklad/app/
 *
 * Bezpečnost: nahrát jde jen soubory z pevného seznamu (žádné .php), takže ani
 * unesený token neumí nahrát nic spustitelného. Přenáší se po částech (velké .ipa).
 */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');

const POVOLENE = [
    'piratsky-poklad.ipa' => true,
    'manifest.plist'      => true,
    'build.json'          => true,
    'index.html'          => true,
    'icon-small.png'      => true,
    'icon-large.png'      => true,
];

function konec(int $kod, array $data): never {
    http_response_code($kod);
    echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

$tokenSoubor = __DIR__ . '/ota-token.txt';
if (!is_file($tokenSoubor)) konec(500, ['chyba' => 'Chybí ota-token.txt na serveru.']);
$token = trim((string) file_get_contents($tokenSoubor));
if ($token === '') konec(500, ['chyba' => 'Prázdný ota-token.txt.']);

$prichozi = $_SERVER['HTTP_X_PUSH_TOKEN'] ?? '';
if (!hash_equals($token, (string) $prichozi)) konec(401, ['chyba' => 'Neplatný token.']);

$appDir = __DIR__ . '/app';
if (!is_dir($appDir) && !mkdir($appDir, 0775, true) && !is_dir($appDir)) {
    konec(500, ['chyba' => 'Nejde vytvořit složku app/.']);
}

// Veřejná adresa složky app/ (z aktuální URL)
$https  = (($_SERVER['HTTPS'] ?? '') === 'on') || (($_SERVER['SERVER_PORT'] ?? '') === '443');
$schema = $https ? 'https' : 'http';
$host   = $_SERVER['HTTP_HOST'] ?? 'www.kukackovi.cz';
$cesta  = rtrim(str_replace('\\', '/', dirname($_SERVER['REQUEST_URI'] ?? '/piratsky-poklad/')), '/');
$base   = "$schema://$host$cesta/app";

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'GET') {
    // GitHub Actions se nejdřív zeptá, kam balíček patří (ověří token i adresu).
    konec(200, ['url' => $base]);
}

$soubor = basename((string) ($_GET['soubor'] ?? ''));
if (!isset(POVOLENE[$soubor])) konec(400, ['chyba' => 'Nepovolený soubor.']);
$prvni  = ($_GET['prvni'] ?? '0') === '1';
$hotovo = ($_GET['hotovo'] ?? '0') === '1';

$cil  = "$appDir/$soubor";
$tmp  = "$cil.part";
$data = file_get_contents('php://input');
if ($data === false) konec(400, ['chyba' => 'Prázdné tělo.']);

$fh = fopen($tmp, $prvni ? 'wb' : 'ab');
if (!$fh) konec(500, ['chyba' => 'Nejde zapisovat.']);
fwrite($fh, $data);
fclose($fh);

if (!$hotovo) konec(200, ['ok' => true, 'cast' => true]);

rename($tmp, $cil);
konec(200, ['ok' => true, 'soubor' => $soubor, 'sha256' => hash_file('sha256', $cil)]);
