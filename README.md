# Cordel Shooter — Lendas do Sertão

Jogo 2D (shoot'em up de rolagem vertical) feito em **Python + Pygame** para a
disciplina **Linguagem de Programação Aplicada**. O jogador controla um
cangaceiro que enfrenta criaturas do folclore brasileiro (Saci, Mula-sem-cabeça
e Boitatá) e, ao final da horda, encara a chefe **Cuca**.

## Como jogar

| Comando | Ação |
|---|---|
| Setas / WASD | Mover o cangaceiro |
| Espaço | Atirar |
| Enter | Confirmar (menu / telas) |
| Esc | Voltar / Sair |

- **Desafio:** sobreviver à horda de monstros que descem atirando.
- **Condição de vitória:** derrotar a Cuca (chefe que aparece após a horda).
- **Condição de derrota:** a barra de vida do herói chegar a zero.
- As pontuações de vitória são salvas em um **ranking** (SQLite) acessível pelo menu.

## Executar a partir do código-fonte

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py
```

> Os assets (PNG) são gerados automaticamente na primeira execução, caso ainda
> não existam, pelo script `tools/gen_assets.py`.

## Gerar o executável (.exe) para Windows — entrega da atividade

Basta executar o script de build (precisa de Python 3.10+ no PATH):

```bat
build.bat
```

O script:
1. cria um ambiente virtual e instala `pygame` e `pyinstaller`;
2. gera os assets PNG;
3. compila o `CordelShooter.exe`;
4. monta a pasta `dist\CordelShooter_entrega` (exe + pasta `asset`);
5. gera o arquivo **`dist\CordelShooter_entrega.zip`** pronto para anexar na entrega.

## Estrutura do projeto

```
CordelShooter/
├── main.py                 # ponto de entrada
├── build.bat               # gera exe + zip de entrega
├── requirements.txt
├── asset/                  # imagens PNG (geradas)
├── tools/
│   └── gen_assets.py       # gerador de sprites e cenários
└── src/
    ├── settings.py         # configurações e atributos das entidades
    ├── assets.py           # localização/carregamento de imagens
    ├── entity.py           # classe base abstrata (herança)
    ├── hero.py             # herói controlado pelo jogador
    ├── monster.py          # monstros do folclore
    ├── boss.py             # chefe (Cuca)
    ├── bullet.py           # projéteis
    ├── scenery.py          # cenário com rolagem (parallax)
    ├── spawner.py          # fábrica de entidades (Factory)
    ├── arbiter.py          # colisões e pontuação (Mediator)
    ├── ranking.py          # ranking persistido em SQLite (Proxy)
    ├── hud.py              # textos e barras de vida
    ├── menu.py             # menu + tela de ranking
    ├── world.py            # fase jogável
    └── game.py             # máquina de estados principal
```

## Sobre originalidade

O código foi escrito do zero para este trabalho. A arquitetura aplica os
conceitos da disciplina (classe abstrata e herança, padrões Factory, Mediator e
Proxy), mas o tema, os sprites, a mecânica (rolagem vertical com chefe) e a
implementação são próprios.
