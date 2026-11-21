# Cordel Shooter - Lendas do Sertão

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
| 1 / 2 / 3 | Trocar o período do dia (manhã / tarde / noite) |

- **Desafio:** sobreviver à horda de monstros que descem atirando.
- **Condição de vitória:** derrotar a Cuca (chefe que aparece após a horda).
- **Condição de derrota:** a barra de vida do herói chegar a zero.
- As pontuações de vitória são salvas em um **ranking** (SQLite) acessível pelo menu.

## Destaques visuais e técnicos

- **Chão pseudo-3D estilo Penguin Adventure (MSX, 1986):** o solo da caatinga
  é desenhado em faixas horizontais com listras alternadas em perspectiva
  (`z = 1/t`) - largas e rápidas perto do jogador, finas e lentas rumo ao
  ponto de fuga -, simulando movimento para frente sem nenhum cálculo 3D real.
  Uma **névoa de distância** funde as listras rente ao horizonte, eliminando
  cintilação e dando profundidade atmosférica.
- **Adereços da caatinga em pseudo-3D:** mandacarus, arbustos secos e pedras
  nascem minúsculos no ponto de fuga, crescem ao se aproximar e escapam pelas
  laterais da tela, presos à mesma "esteira" de profundidade do chão.
- **Períodos do dia:** o cenário (céu, chão, nuvens e adereços) muda de paleta
  conforme o relógio do computador - manhã, tarde ou noite - e pode ser
  alternado em jogo pelas teclas 1/2/3.
- **Nuvens procedurais dinâmicas:** geradas em tempo de execução, rolam em
  direção ao horizonte com parallax, tanto no menu quanto na fase.
- **Trilha sonora e efeitos:** música de fundo e SFX de tiro, dano e bônus via
  `pygame.mixer`.
- **Delta time:** velocidades e temporizadores escalados pelo tempo real do
  frame, mantendo o ritmo do jogo estável em qualquer máquina.
- **Easter eggs:** o ET de Varginha aparece para socorrer o herói com pouca
  vida - e dizem que um código famoso digitado no menu desbloqueia o
  *Modo Cangaço*...

## Executar a partir do código-fonte

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python main.py
```

> Os assets (PNG) são gerados automaticamente na primeira execução, caso ainda
> não existam, pelo script `tools/gen_assets.py`.

## Gerar o executável (.exe) para Windows - entrega da atividade

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
    ├── scenery.py          # céu, chão pseudo-3D e adereços da caatinga
    ├── clouds.py           # nuvens procedurais dinâmicas
    ├── specials.py         # ET de Varginha e bônus de vida
    ├── sounds.py           # música de fundo e efeitos sonoros
    ├── cheats.py           # estado dos easter eggs
    ├── konami.py           # detector de sequência de teclas no menu
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

## Melhorias já implementadas

As sugestões mapeadas na revisão de código anterior foram todas incorporadas:

1. **Invencibilidade temporária (i-frames)** - após receber dano, o herói fica
   imune por ~1 segundo (`INVINCIBILITY_FRAMES`) com o sprite piscando.
2. **Tabela de ranking alinhada** - Nome, Pontos e Data são renderizados em
   colunas de coordenada X fixa na tela de Top 10.
3. **Gerenciador de contexto no banco** - `ScoreDB` implementa
   `__enter__`/`__exit__`, permitindo `with ScoreDB() as db:` com fechamento
   garantido da conexão SQLite.
4. **Importações organizadas (PEP 8)** - imports movidos para o topo dos
   módulos.
5. **Trilha sonora e SFX** - música de fundo em loop e efeitos de tiro, dano e
   bônus via `pygame.mixer` (`sounds.py`).
6. **Delta time** - o `dt` de `clock.tick(settings.FPS)` escala todas as
   velocidades e temporizadores, desacoplando o jogo da taxa de quadros.

## Implementações futuras

- Fases múltiplas com dificuldade progressiva e novos chefes do folclore.
- Obstáculos no chão pseudo-3D que interagem com o herói (desviar/colidir),
  aproximando ainda mais a jogabilidade do Penguin Adventure.
- Power-ups de tiro (leque, rajada, cadência) soltos pelos monstros.

