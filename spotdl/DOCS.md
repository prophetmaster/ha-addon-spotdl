# spotDL

L'interface web de [spotDL](https://github.com/spotDL/spotify-downloader) dans Home Assistant.
Colle un lien Spotify (titre, album, playlist) ou cherche un titre, puis télécharge-le.
Les fichiers arrivent dans `/media/spotdl`, où Music Assistant et le navigateur de médias de
Home Assistant les trouvent.

## Utilisation

1. Démarre l'addon.
2. Ouvre **spotDL** dans la barre latérale de Home Assistant.
3. Colle un lien `https://open.spotify.com/...` dans la recherche, ou tape un titre, puis Entrée.
4. Clique sur le bouton de téléchargement. La progression s'affiche sous l'icône de nuage,
   et le journal de l'addon écrit « Finished … » à la fin de chaque lien.

Le format et la qualité se règlent dans les options de l'addon : la roue dentée de
l'interface web ne les change pas.

Une playlist doit être publique. Les titres likés sont privés : copie-les d'abord dans une
playlist publique.

## Options

| Option | Rôle |
|---|---|
| `output_dir` | Dossier de destination, obligatoirement dans `/media`. |
| `format` | `mp3`, `flac`, `ogg`, `opus`, `m4a` ou `wav`. |
| `bitrate` | Qualité de l'encodage. `320k` est le maximum en MP3. |
| `client_id`, `client_secret` | Ton propre identifiant Spotify (voir ci-dessous). Facultatif, mais conseillé. |
| `log_level` | Détail du journal de l'addon. |

## Ton propre identifiant Spotify

Sans identifiant, spotDL partage celui de tous ses utilisateurs, et Spotify le bloque souvent
pendant des heures. L'interface reste alors sur « Loading ». Avec le tien :

1. Va sur <https://developer.spotify.com/dashboard> et clique sur **Create app**.
2. Redirect URI : `http://127.0.0.1:9900/`. Coche **Web API**, puis **Save**.
3. Dans **Settings**, copie le **Client ID** et le **Client secret** dans les options de l'addon.
4. Redémarre l'addon.

## Accès direct

Le port 8800 est désactivé par défaut. Si tu l'actives, l'interface est accessible sur
`http://<ip de home assistant>:8800` **sans mot de passe** : à éviter si ton réseau n'est pas privé.

## Bon à savoir

- spotDL ne télécharge pas depuis Spotify : il lit les infos du titre sur Spotify, puis
  récupère l'audio sur YouTube Music.
- Les conditions d'utilisation de Spotify et de YouTube interdisent le téléchargement.
  Garde les fichiers pour toi, ne les partage pas.
