# spotDL pour Home Assistant

Un dépôt d'addons Home Assistant avec un seul addon : l'interface web de
[spotDL](https://github.com/spotDL/spotify-downloader), dans la barre latérale de Home Assistant.
La musique téléchargée arrive dans `/media/spotdl`.

Fonctionne sur Home Assistant OS ou Supervised, en 64 bits (amd64, aarch64 : PC, mini-PC, Raspberry Pi 4/5).

## Installation

1. Dans Home Assistant : **Paramètres → Modules complémentaires → Boutique → ⋮ → Dépôts**,
   colle `https://github.com/prophetmaster/ha-addon-spotdl`, puis **Ajouter**.
2. Recharge la page de la boutique : spotDL apparaît en bas.
3. Installe **spotDL**. La première installation construit l'image sur ta machine : compte
   quelques minutes sur un Raspberry Pi.
4. Démarre-le et coche **Afficher dans la barre latérale**.

La documentation de l'addon est dans [spotdl/DOCS.md](spotdl/DOCS.md).

## Comment ça marche

`spotdl/run.py` lance `spotdl web` avec les options de l'addon. L'interface de spotDL écrit des
adresses absolues (`/assets/…`, `/client/…`) ; derrière l'ingress de Home Assistant, `run.py`
les préfixe avec l'en-tête `X-Ingress-Path`, dans les pages comme dans le flux d'événements.
`run.py` remplace aussi la route de téléchargement de l'interface, qui dans spotDL 4.6.0 n'accepte
que des liens de titres : albums, playlists et artistes passent, et le téléchargement continue
quand on quitte la page. spotDL est figé à la version 4.6.0 dans le `Dockerfile` : ces réécritures dépendent de ses gabarits,
donc revérifie-les en changeant de version.
