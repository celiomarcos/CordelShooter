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

## Implementações Futuras

Com base em uma revisão detalhada do código-fonte e da arquitetura do jogo, foram mapeadas as seguintes sugestões de melhorias estruturais, visuais e de jogabilidade para futuras versões:

1. **Sistema de Invencibilidade Temporária (i-frames) para o Herói**:
   * **Objetivo**: Evitar mortes instantâneas por colisão contínua ou rajadas de tiros acumulados em poucos frames.
   * **Ideia**: Conceder ao herói um timer de imunidade temporária (ex: 60 frames / 1 segundo) após receber dano, fazendo seu sprite piscar na tela e ignorando novas colisões de dano nesse intervalo.

2. **Alinhamento Preciso da Tabela de Ranking**:
   * **Objetivo**: Garantir que as colunas na tela de Top 10 se alinhem perfeitamente de forma vertical.
   * **Ideia**: Renderizar os campos de Nome, Pontuação e Data separadamente no HUD em coordenadas X fixas (ex: `cx - 220`, `cx - 40` e `cx + 80`), em vez de desenhar uma única string formatada com espaços em uma fonte de tamanho variável (Verdana).

3. **Gerenciador de Contexto para a Classe de Banco de Dados (`ScoreDB`)**:
   * **Objetivo**: Garantir o fechamento correto das conexões com o SQLite e evitar concorrência ou vazamento de recursos.
   * **Ideia**: Implementar os métodos `__enter__` e `__exit__` em `ScoreDB` (`ranking.py`), permitindo a utilização segura e Pythonica através de blocos `with ScoreDB() as db:`.

4. **Refatoração e Limpeza de Importações (PEP 8)**:
   * **Objetivo**: Tornar o código mais limpo e legível.
   * **Ideia**: Mover as importações inline/tardias encontradas em `spawner.py` (como `random` e `ET`) para o topo do arquivo, uma vez que não há risco real de importação circular.

5. **Trilha Sonora e Efeitos Sonoros (SFX)**:
   * **Objetivo**: Aumentar a imersão e dar feedback sensorial ao jogador.
   * **Ideia**: Utilizar o módulo `pygame.mixer` para tocar uma música de fundo com sonoridade de sertanejo/cordel ou estilo 8-bit em loop, além de efeitos sonoros rápidos ao atirar, acertar inimigos, coletar vida ou no fim do jogo.

6. **Desacoplamento de Frames por Segundo (Delta Time)**:
   * **Objetivo**: Tornar a velocidade de movimentação e do jogo consistente em qualquer computador, independente da taxa de quadros (FPS) que o computador consiga processar.
   * **Ideia**: Obter o tempo delta (`dt`) a partir de `clock.tick(settings.FPS)` e utilizá-lo como multiplicador de todas as velocidades e temporizadores físicos do jogo.

