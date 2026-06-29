# Diagrama de Classes — Cordel Shooter

Visão geral da arquitetura orientada a objetos do jogo. `Entity` é a
classe base abstrata; as demais entidades a especializam (herança). Os
padrões **Factory** (`Spawner`), **Mediator** (`Arbiter`) e **Proxy**
(`ScoreDB`) organizam criação, interação e persistência.

```mermaid
classDiagram
    class Entity {
        <<abstract>>
        +str name
        +Surface surf
        +Rect rect
        +int health
        +int damage
        +int score
        +str last_hit_by
        +is_alive() bool
        +collides_with(other) bool
        +update()* 
    }

    class Hero {
        +int cooldown
        +update()
        +try_shoot() HeroBullet
    }
    class Monster {
        +int cooldown
        +update()
        +try_shoot() MonsterBullet
    }
    class Boss {
        +bool entering
        +update()
        +try_shoot() BossBullet[]
    }
    class HeroBullet {
        +update()
    }
    class MonsterBullet {
        +update()
    }
    class BossBullet
    class Scenery {
        +update()
    }

    Entity <|-- Hero
    Entity <|-- Monster
    Entity <|-- Boss
    Entity <|-- HeroBullet
    Entity <|-- MonsterBullet
    Entity <|-- Scenery
    MonsterBullet <|-- BossBullet

    class Spawner {
        <<Factory>>
        +background() Scenery[]
        +hero() Hero
        +random_monster() Monster
        +boss() Boss
    }
    class Arbiter {
        <<Mediator>>
        +resolve_collisions(entities, hero)
        +collect_dead(entities, hero) int
    }
    class ScoreDB {
        <<Proxy>>
        +save(name, score)
        +top(limit) list
        +close()
    }

    class World {
        +Hero hero
        +list entities
        +int score
        +run() tuple
    }
    class Menu {
        +run() str
        +show_ranking()
    }
    class Game {
        +run()
    }

    Hero ..> HeroBullet : cria
    Monster ..> MonsterBullet : cria
    Boss ..> BossBullet : cria
    Spawner ..> Hero : cria
    Spawner ..> Monster : cria
    Spawner ..> Boss : cria
    Spawner ..> Scenery : cria
    World o-- Entity : gerencia
    World *-- Hero
    World ..> Spawner
    World ..> Arbiter
    Arbiter ..> Entity : resolve
    Menu ..> ScoreDB
    Game *-- Menu
    Game ..> World
    Game ..> ScoreDB
```

## Condições do jogo (atividade)

- **Controle do jogador:** `Hero.update()` (setas/WASD) e `Hero.try_shoot()` (espaço).
- **Desafio:** `Monster`/`Boss` descem e atiram; `Arbiter` resolve as colisões.
- **Vitória:** derrotar a `Boss` (Cuca) — `World.run()` retorna `"win"`.
- **Derrota:** vida do `Hero` chega a zero — `World.run()` retorna `"lose"`.
