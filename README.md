# The-Battle-of-Valoran
## 简介
- 使用了python(3.8版本)的pygame库编写的自走棋小游戏，以拳头公司的**云顶之弈**为模板，简化为了3v3的二维自走棋。
- 前后共有3个版本，以最后一个版本为例，仿照了云顶之弈S3的英雄卡池，设计了共29个英雄、16种羁绊、9种基础武器以及45种进阶武器。
## 规则简述
- 游戏分左右双方，双方均具有3名英雄，不同的英雄拥有不同的基础属性、羁绊组合和技能。
- 游戏一开始，各名英雄的攻击目标为其对位英雄，根据物理攻击力、攻击速度、暴击率、暴击倍数、闪避率等参数来执行普通攻击。
- 英雄进行普通攻击造成伤害和自身受到伤害都会获得法力值，当法力值达到上限值就会施放技能。
- 武器系统：一开始每个英雄会在9种基础武器中随机获得一个武器并获得相应的属性加成，当英雄的生命值低于75%时会获得第二个随机基础武器，根据前后两个基础武器的组合关系合成为进阶武器，不同的进阶武器有不同的效果。
- 羁绊系统：每个英雄都具有两个羁绊，一个称为种族羁绊，另一个称为职业羁绊，当同一队伍中出现同样的羁绊时，会触发特殊的效果。
## 截图
![](https://github.com/Flamingo6947/The-Battle-of-Valoran/raw/截图/bov_pic_1.png)
 
