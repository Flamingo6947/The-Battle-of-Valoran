import pygame
import sys
import math
from time import sleep
from random import randint
from random import shuffle
from pygame.locals import *
from abc import ABCMeta, abstractmethod

# 版本
version = [3]
# 颜色
if True:
	white = (255, 255, 255)
	black = (0, 0, 0)
	purple = (197, 108, 235)
	dark_purple = (93, 23, 148)
	red = (255, 0, 0)
	red2 = (255, 11, 79)
	light_red = (241, 83, 83)
	dark_red = (132, 41, 8)
	dark_red2 = (171, 39, 37)
	green = (80, 205, 74)
	green2 = (69, 167, 71)
	green3 = (169, 255, 181)
	light_green = (88, 245, 183)
	light_green2 = (172, 245, 155)
	light_green3 = (0, 255, 121)
	white_green = (231, 243, 206)
	dark_green = (5, 98, 95)
	dark_green2 = (7, 131, 131)
	gary_green = (145, 183, 174)
	blue = (0, 0, 255)
	blue2 = (22, 188, 245)
	white_blue = (185,239,255)
	light_blue = (58, 223, 250)
	dark_blue = (11, 47, 130)
	gray_blue = (73, 137, 215)
	gray_blue2 = (77, 76, 99)
	bule_purple = (121, 136, 235)
	gray = (192, 192, 192)
	light_gray = (178, 177, 219)
	dark_gray = (68, 75, 89)
	orange = (253, 132, 34)
	gray_orange = (147, 143, 131)
	orange_yellow = (241, 204, 118)
	orange_red = (217, 77, 9)
	orange_red2 = (250, 93, 26)
	dark_orange = (126, 105, 74)
	yellow = (255, 255, 0)
	light_yellow = (238, 211, 181)
	light_yellow2 = (255, 250, 213)
	dark_yellow = (169, 165, 80)
	yellow_green = (209, 235, 61)
	cyan = (41, 173, 195)
	dark_cyan = (11, 165, 152)
	light_cyan = (23, 239, 229)
	white_cyan = (180, 242, 242)
	pink = (202, 129, 169)
	pink2 = (167, 61, 127)
	dark_pink = (165, 29, 131)
	silver = (178, 177, 219)

# 背景色
sky_color = [black]
# 左右方分值
point = [10 for _ in range(2)]
# 回合数
Round = [0]
# 时间修正系数
time_correction = [3]
# 战斗机目标坐标(共36个):x|y|是否被选做目的点
warcraft_xy = [[[[[0,0,False] for _ in range(3)] for _ in range(2)] for _ in range(3)] for _ in range(2)]
for a in range(2):  # a为左右方|b为目标英雄位置|c为左右侧|d为上中下
	for b in range(3):
		for c in range(2):
			for d in range(3):
				warcraft_xy[a][b][c][d][0] = 181 + 442 * a + 366 * c
				warcraft_xy[a][b][c][d][1] = 50 + 230 * b + 55 * d
# 最大值算法
def Max(a,b):
	if a >= b:
		return a
	else:
		return b

# 持续时间计数值
class Time_count(object):
	def __init__(self):
		self.value = 0               # 持续时间计数值
	# 持续时间计算
	def Duration(self, time):    
		self.value += 1
		if self.value < int(time * 100 / time_correction[0]):
			return False
		else:
			self.value = 0
			return 	True   # end

# 游戏全局
class Game(object):
	def __init__(self,cp_number,screen):
		self.time = 0
		self.time_count = Time_count()
		self.urf = [0,50,Time_count()]
		self.LR = [[None for _ in range(3)] for _ in range(2)]
		self.LR_ui = [[None for _ in range(3)] for _ in range(2)]
		self.result = None
		self.LR_rela = [{'光' : 0, '极地' : 0, '森林' : 0, '水晶' : 0, '海洋' : 0, '钢铁' : 0, '沙漠' : 0, '地狱火' : 0, '影' : 0\
		 ,'游侠' : 0, '掠食者' : 0, '秘术师' : 0, '守护神' : 0, '法师' : 0, '刺客' : 0, '狂战士' : 0, '大元素使' : 0\
		 , '恕瑞玛之皇' : 0 , '太阳圆盘' : 0, '斗士' : 0, '银月' : 0, '剧毒' : 0, '剑士' : 0, '枪手' : 0, '云霄' : 0, \
		 '雷霆' : 0, '忍者' : 0, '忍剑士' : 0, '银河机神' : 0, '奥德赛' : 0, '未来战士' : 0, '星神' : 0, '星之守护者' : 0, \
		 '暗星' : 0, '爆破专家' : 0, '源计划' : 0, '护卫' : 0, '星舰龙神' : 0, '虚空' : 0, '先锋' : 0, '银河魔装机神' : 0, '异星人' : 0} for _ in range(2)]
		k = 0
		self.Kindred_sign_flag = False
		self.warcraft_flag = False
		self.desert_flag = [[False,False],[False,False]]
		self.SolarDisk = [False,Time_count(),2,None,None]
		self.screen = screen
		# 银月羁绊标志
		self.moon_flag = [[False,0,Time_count(),0] for _ in range(2)]
		# 海洋羁绊标志
		self.sea_flag = [[False,0,Time_count()] for _ in range(2)]
		# 未来战士羁绊标志
		self.future_flag = [[False,0,Time_count()] for _ in range(2)]
		# 银河机神羁绊标志
		self.MechWarrior_flag = [[False,0,[Time_count(),1],[False,False],None] for _ in range(2)] # 使能|人数|合体计时|合体/解体标志位|合体位置原英雄存储
		# 波比屏障标志
		self.obstacle_flag = [False,None]
		# 重置魔偶、皮克斯、提伯斯
		golem.__init__()
		pix.__init__()
		tibbers.__init__()
		for i in range(2):
			for j in range(3):
				self.LR[i][j] = champion_dic.get(cp_number[k])
				k += 1
				self.LR[i][j].__init__()
				self.LR[i][j].position = i # 0表示L，1表示R
				self.LR[i][j].pos_num = j
				self.LR[i][j].game = self
				if version[0] == 1:
					if self.LR[i][j].champion.name == 'Azir':
						self.desert_flag[i][0] = True
					# 重置沙兵
					for s in range(3):
						sand[s].flag = False
						sand[s].time_count.value = 0
					# 初始化
					tide.__init__()
					fireball.__init__()
				elif version[0] == 2:
					# 重置月之驻灵
					for m in range(3):
						moonbattery[m].__init__()
						moonbattery[m].pos_num = m
					# 设置魔偶
					if self.LR[i][j].champion.name == 'Orianna':
						golem.Orianna = self.LR[i][j]
						golem.flag = True
						golem.position = self.LR[i][j].position
						golem.pos_num = self.LR[i][j].pos_num
						golem.Init()
				elif version[0] == 3:
					# 重置炮台
					for b in range(3):
						battery[b].__init__()
						battery[b].pos_num = b
					# 设置皮克斯
					if self.LR[i][j].champion.name == 'Lulu':
						pix.Lulu = self.LR[i][j]
						pix.target = self.LR[i][j]
						pix.flag = True
						pix.position = self.LR[i][j].position
						pix.pos_num = self.LR[i][j].pos_num
						pix.Init()
					# 设置战斗机
					if self.LR[i][j].champion.name == 'AurelionSol':
						# 占位初始化
						for a in range(2):
							for b in range(3):
								for c in range(2):
									for d in range(3):
										warcraft_xy[a][b][c][d][2] = False
						self.warcraft_flag = True
						for num in range(6):
							warcraft[num].AurelionSol = self.LR[i][j]
							warcraft[num].game = self
							warcraft[num].flag = False
							warcraft[num].position = self.LR[i][j].position
							warcraft[num].pos_num = self.LR[i][j].pos_num
							# 舱位
							warcraft[num].Orig()
				# 初始化
				# wand.__init__()
		# 确定初始攻击目标
		for i in range(3):
			self.LR[0][i].enemy = self.LR[1][i]
			self.LR[1][i].enemy = self.LR[0][i]
		for i in range(2):
			for j in range(3):
				for k in range(3):
					self.LR[i][j].friend[k] = self.LR[i][k]
		self.Rela_judg()
		self.Rela_record()
		self.Rela_effect()
		for i in range(2):
			for j in range(3):
				if version[0] == 1:
					# 千珏之印标记
					if self.LR[i][j].champion.name == 'Kindred' and not self.Kindred_sign_flag:
						self.LR[~i+2][randint(0,2)].flag.special_flag.Kindred_sign = True
						self.Kindred_sign_flag = True
						
				self.LR_ui[i][j] = Champion_Interface(screen,self.LR[i][j],self)
				self.LR_ui[i][j].Bg()
				self.LR_ui[i][j].Draw([0,0])
	# 判断游戏结束
	def Finish_judg(self):
		if (self.LR[0][0].flag.condition_flag.death_flag and self.LR[0][1].flag.condition_flag.death_flag and self.LR[0][2].flag.condition_flag.death_flag) and (not(self.LR[1][0].flag.condition_flag.death_flag and self.LR[1][1].flag.condition_flag.death_flag and self.LR[1][2].flag.condition_flag.death_flag)):
			self.result = 'R Win!'
		elif (not(self.LR[0][0].flag.condition_flag.death_flag and self.LR[0][1].flag.condition_flag.death_flag and self.LR[0][2].flag.condition_flag.death_flag)) and (self.LR[1][0].flag.condition_flag.death_flag and self.LR[1][1].flag.condition_flag.death_flag and self.LR[1][2].flag.condition_flag.death_flag):
			self.result  = 'L Win!'
		elif(self.LR[0][0].flag.condition_flag.death_flag and self.LR[0][1].flag.condition_flag.death_flag and self.LR[0][2].flag.condition_flag.death_flag) and (self.LR[1][0].flag.condition_flag.death_flag and self.LR[1][1].flag.condition_flag.death_flag and self.LR[1][2].flag.condition_flag.death_flag):
			self.result  = 'Dogfall!'
		else:
			self.result  = 'Continue'
		return self.result
	# 计时与海牛加时赛
	def Urf(self,screen):
		if self.time_count.Duration(1):
			self.time += 1
		if self.urf[2].Duration(self.urf[1]):
			self.urf[1] = 5
			self.urf[0] += 1
			for i in range(2):
				for j in range(3):
					if (not self.LR[i][j].flag.condition_flag.death_flag) and (not self.LR[i][j].flag.condition_flag.miss_flag[0]):
						if self.LR[i][j].champion.name == 'Jhin':
							self.LR[i][j].As2cr(1.5)
						else:
							self.LR[i][j].champion.attack_attribute.attack_speed *= 1.5
						self.LR[i][j].champion.attack_attribute.spell_power += 0.05
						self.LR[i][j].champion.defensive_attribute.Add_tenacity(0.4)
	# 判断羁绊
	def Rela_judg(self):
		for i in range(2):
			for j in range(3):
				if self.LR[i][j].champion.relatedness.element[0] == '黯焰':
					self.LR_rela[i]['黯焰'] = 4
					self.LR_rela[i]['地狱火'] += 1
					self.LR_rela[i]['影'] += 1
				else:
					self.LR_rela[i][self.LR[i][j].champion.relatedness.element[0]] += 1
				if self.LR[i][j].champion.relatedness.profession[0] == '忍剑士':
					self.LR_rela[i]['忍剑士'] = 1
					self.LR_rela[i]['忍者'] += 1
					self.LR_rela[i]['剑士'] += 1
				else:	
					self.LR_rela[i][self.LR[i][j].champion.relatedness.profession[0]] += 1
				if self.LR[i][j].champion.relatedness.profession[0] == '大元素使':
					self.LR_rela[i][self.LR[i][j].champion.relatedness.element[0]] += 1
					self.LR_rela[i]['大元素使'] = 4
				elif self.LR[i][j].champion.relatedness.profession[0] == '恕瑞玛之皇':
					self.LR_rela[i][self.LR[i][j].champion.relatedness.element[0]] += 1
					self.LR_rela[i]['恕瑞玛之皇'] = 4
				elif self.LR[i][j].champion.relatedness.profession[0] == '星舰龙神':
					self.LR_rela[i]['星舰龙神'] = 3
				elif self.LR[i][j].champion.relatedness.element[0] == '异星人':
					self.LR_rela[i]['异星人'] = 3
	# 记录羁绊
	def Rela_record(self):
		# 记录羁绊	
		for i in range(2):
			for j in range(3):
				self.LR[i][j].champion.relatedness.element[1] = self.LR_rela[i][self.LR[i][j].champion.relatedness.element[0]]
				if self.LR[i][j].champion.relatedness.element[0] == '银河魔装机神':
					self.LR[i][j].champion.relatedness.element[1] = 3
				elif self.LR[i][j].champion.relatedness.element[0] == '虚空':
					self.LR[i][j].champion.relatedness.element[1] = 2
				self.LR[i][j].champion.relatedness.profession[1] = self.LR_rela[i][self.LR[i][j].champion.relatedness.profession[0]]
				if self.LR[i][j].champion.relatedness.profession[0] == '先锋':
					self.LR[i][j].champion.relatedness.profession[1] = 2
				if self.LR[i][j].champion.relatedness.extra[0] != 'None':
					self.LR[i][j].champion.relatedness.extra[1] = self.LR_rela[i][self.LR[i][j].champion.relatedness.extra[0]]
	# 处理羁绊效果
	def Rela_effect(self):
		for i in range(2):
			# 群体效果
			# 	沙漠
			sm_n = self.LR_rela[i]['沙漠']
			if sm_n > 1:
				for j in range(3):
					self.LR[~i+2][j].champion.defensive_attribute.armor *= (1 - rela_dic['沙漠'][1][sm_n - 2])
			# 	秘术师
			mss_n = self.LR_rela[i]['秘术师']
			if mss_n > 1:
				for j in range(3):
					self.LR[i][j].champion.defensive_attribute.spell_resistance += rela_dic['秘术师'][1][mss_n - 2]
			#	海洋
			hy_n = self.LR_rela[i]['海洋']
			if hy_n > 1:
				self.sea_flag[i][0] = True
				self.sea_flag[i][1] = hy_n - 2
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '海洋':
						self.LR[i][j].flag.rela_flag['海洋'][0] = True
						self.LR[i][j].flag.rela_flag['海洋'][1] = rela_dic['海洋'][1][hy_n - 2]
			#	银月
			yy_n = self.LR_rela[i]['银月']
			if yy_n > 1:
				self.moon_flag[i][0] = True
				self.moon_flag[i][1] = yy_n - 2
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '银月':
						self.LR[i][j].flag.rela_flag['银月'][0] = True
						self.LR[i][j].flag.rela_flag['银月'][1] = rela_dic['银月'][1][yy_n - 2]
			# 	云霄
			yx2_n = self.LR_rela[i]['云霄']
			if yx2_n > 1:
				for j in range(3):
					self.LR[i][j].champion.defensive_attribute.dodge_mechanism.Add_dodge(rela_dic['云霄'][1][yx2_n - 2])
			#	未来战士
			wlzs_n = self.LR_rela[i]['未来战士']
			if wlzs_n > 1:
				self.future_flag[i][0] = True
				self.future_flag[i][1] = wlzs_n - 2
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '未来战士':
						self.LR[i][j].flag.rela_flag['未来战士'][0] = True
						self.LR[i][j].flag.rela_flag['未来战士'][1] = rela_dic['未来战士'][1][wlzs_n - 2]
			#	星神
			xs_n = self.LR_rela[i]['星神']
			if xs_n > 1:
				for j in range(3):
					self.LR[i][j].flag.rela_flag['星神'][3] = True
					self.LR[i][j].flag.rela_flag['星神'][1] = rela_dic['星神'][1][xs_n - 2]
					if self.LR[i][j].champion.relatedness.element[0] == '星神':
						self.LR[i][j].flag.rela_flag['星神'][0] = True
						
			# 个体效果
			#	守护神
			shs_n = self.LR_rela[i]['守护神']
			if shs_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '守护神':
						self.LR[i][j].champion.defensive_attribute.armor += rela_dic['守护神'][1][shs_n - 2]
			#	刺客
			ck_n = self.LR_rela[i]['刺客']
			if ck_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '刺客':
						self.LR[i][j].champion.attack_attribute.crit_mechanism.crit += rela_dic['刺客'][1][ck_n - 2][0]
						self.LR[i][j].champion.attack_attribute.crit_mechanism.crit_multiple += rela_dic['刺客'][1][ck_n - 2][1]
			# 	法师
			fs_n = self.LR_rela[i]['法师']
			if fs_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '法师':
						self.LR[i][j].champion.attack_attribute.spell_power += rela_dic['法师'][1][fs_n - 2]
			# 	极地
			jd_n = self.LR_rela[i]['极地']
			if jd_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '极地':
						self.LR[i][j].flag.rela_flag['极地'][0] = True
						self.LR[i][j].flag.rela_flag['极地'][1] = rela_dic['极地'][1][jd_n - 2]
			# 	钢铁
			gt_n = self.LR_rela[i]['钢铁']
			if gt_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '钢铁':
						self.LR[i][j].flag.rela_flag['钢铁'][0] = True
						self.LR[i][j].flag.rela_flag['钢铁'][1] = rela_dic['钢铁'][1][gt_n - 2]
			#	森林
			sl_n = self.LR_rela[i]['森林']
			if sl_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '森林':
						self.LR[i][j].flag.rela_flag['森林'][0] = True
						self.LR[i][j].flag.rela_flag['森林'][1] = rela_dic['森林'][1][sl_n - 2]
			# 	光
			g_n = self.LR_rela[i]['光']
			if g_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '光':
						self.LR[i][j].flag.rela_flag['光'][0] = True
						self.LR[i][j].flag.rela_flag['光'][1] = rela_dic['光'][1][g_n - 2]
			# 	水晶
			sj_n = self.LR_rela[i]['水晶']
			if sj_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '水晶':
						self.LR[i][j].flag.rela_flag['水晶'][0] = True
						self.LR[i][j].flag.rela_flag['水晶'][1] = rela_dic['水晶'][1][sj_n - 2]
			# 	掠食者
			lsz_n = self.LR_rela[i]['掠食者']
			if lsz_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '掠食者':
						self.LR[i][j].flag.rela_flag['掠食者'][0] = True
						self.LR[i][j].flag.rela_flag['掠食者'][1] = rela_dic['掠食者'][1][lsz_n - 2]
			# 	狂战士
			kzs_n = self.LR_rela[i]['狂战士']
			if kzs_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '狂战士':
						self.LR[i][j].flag.rela_flag['狂战士'][0] = True
						self.LR[i][j].flag.rela_flag['狂战士'][1] = rela_dic['狂战士'][1][kzs_n - 2]
			if kzs_n == 3:
				for k in range(3):
					self.LR[i][k].champion.attack_attribute.AD += rela_dic['狂战士'][1][3]
			# 	影
			y_n = self.LR_rela[i]['影']
			if y_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] in ('影','黯焰'):
						self.LR[i][j].flag.rela_flag['影'][0] = True
						self.LR[i][j].flag.rela_flag['影'][1] = rela_dic['影'][1][y_n - 2]
			# 	地狱火
			dyh_n = self.LR_rela[i]['地狱火']
			if dyh_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] in ('地狱火','黯焰'):
						self.LR[i][j].flag.rela_flag['地狱火'][0] = True
						self.LR[i][j].flag.rela_flag['地狱火'][1] = rela_dic['地狱火'][1][dyh_n - 2]
			# 	游侠
			yx_n = self.LR_rela[i]['游侠']
			if yx_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '游侠':
						self.LR[i][j].flag.rela_flag['游侠'][0] = True
						self.LR[i][j].flag.rela_flag['游侠'][1] = rela_dic['游侠'][1][yx_n - 2]
			#	斗士
			ds_n = self.LR_rela[i]['斗士']
			if ds_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '斗士':
						self.LR[i][j].flag.rela_flag['斗士'][0] = True
						self.LR[i][j].flag.rela_flag['斗士'][1] = rela_dic['斗士'][1][ds_n - 2]
						self.LR[i][j].champion.hp.max_value += rela_dic['斗士'][1][ds_n - 2]
						self.LR[i][j].champion.hp.value += rela_dic['斗士'][1][ds_n - 2]
			#	剧毒
			jd2_n = self.LR_rela[i]['剧毒']
			if jd2_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '剧毒':
						self.LR[i][j].flag.rela_flag['剧毒'][0] = True
						self.LR[i][j].flag.rela_flag['剧毒'][1] = jd2_n
			#	雷霆
			lt_n = self.LR_rela[i]['雷霆']
			if lt_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '雷霆':
						self.LR[i][j].flag.rela_flag['雷霆'][0] = True
						self.LR[i][j].flag.rela_flag['雷霆'][1] = rela_dic['雷霆'][1][lt_n - 2]
			# 	枪手
			qs_n = self.LR_rela[i]['枪手']
			if qs_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '枪手':
						self.LR[i][j].flag.rela_flag['枪手'][0] = True
						self.LR[i][j].flag.rela_flag['枪手'][1] = rela_dic['枪手'][1][qs_n - 2]
			# 	剑士
			js_n = self.LR_rela[i]['剑士']
			if js_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] in ('剑士','忍剑士'):
						self.LR[i][j].flag.rela_flag['剑士'][0] = True
						self.LR[i][j].flag.rela_flag['剑士'][1] = rela_dic['剑士'][1][js_n - 2]
			# 	忍者
			rz_n = self.LR_rela[i]['忍者']
			if rz_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] in ('忍者','忍剑士'):
						self.LR[i][j].flag.rela_flag['忍者'][0] = True
						self.LR[i][j].flag.rela_flag['忍者'][1] = rela_dic['忍者'][1][rz_n - 2]
				self.Ninja_buff(self.LR[i][0],rela_dic['忍者'][1][rz_n - 2])
			# 	爆破专家
			bpzj_n = self.LR_rela[i]['爆破专家']
			if bpzj_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '爆破专家':
						self.LR[i][j].flag.rela_flag['爆破专家'][0] = True
						self.LR[i][j].flag.rela_flag['爆破专家'][1] = rela_dic['爆破专家'][1][bpzj_n - 2]
			# 	奥德赛
			ads_n = self.LR_rela[i]['奥德赛']
			if ads_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '奥德赛':
						self.LR[i][j].flag.rela_flag['奥德赛'][0] = True
						self.LR[i][j].flag.rela_flag['奥德赛'][1] = rela_dic['奥德赛'][1][ads_n - 2]
				self.LR[i][j].champion.relatedness.Odyssey(self,i,0,None)
			# 	星之守护者
			xzshz_n = self.LR_rela[i]['星之守护者']
			if xzshz_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '星之守护者':
						self.LR[i][j].flag.rela_flag['星之守护者'][0] = True
						self.LR[i][j].flag.rela_flag['星之守护者'][1] = rela_dic['星之守护者'][1][xzshz_n - 2]
			# 	源计划
			yjh_n = self.LR_rela[i]['源计划']
			if yjh_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '源计划':
						self.LR[i][j].flag.rela_flag['源计划'][0] = True
						self.LR[i][j].flag.rela_flag['源计划'][1] = rela_dic['源计划'][1][yjh_n - 2]
						self.LR[i][j].flag.rela_flag['源计划'][3] = yjh_n
			#	暗星
			szx_n = self.LR_rela[i]['暗星']
			if szx_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '暗星':
						self.LR[i][j].flag.rela_flag['暗星'][0] = True
						self.LR[i][j].flag.rela_flag['暗星'][1] = rela_dic['暗星'][1][szx_n - 2]
			#	银河机神
			yhjs_n = self.LR_rela[i]['银河机神']
			if yhjs_n > 1:
				self.MechWarrior_flag[i][0] = True
				self.MechWarrior_flag[i][1] = yhjs_n
				for j in range(3):
					if self.LR[i][j].champion.relatedness.element[0] == '银河机神':
						self.LR[i][j].flag.rela_flag['银河机神'][0] = True
						self.LR[i][j].flag.rela_flag['银河机神'][2][0] = True
						self.LR[i][j].condition.miss.Add_miss(self.LR[i][j], 100)
			#	护卫
			hw_n = self.LR_rela[i]['护卫']
			if hw_n > 1:
				for j in range(3):
					if self.LR[i][j].champion.relatedness.profession[0] == '护卫':
						self.LR[i][j].flag.rela_flag['护卫'][0] = True
						self.LR[i][j].flag.rela_flag['护卫'][2][0] = True
						self.LR[i][j].flag.rela_flag['护卫'][1] = rela_dic['护卫'][1][hw_n - 2]
						self.LR[i][j].champion.defensive_attribute.armor += self.LR[i][j].flag.rela_flag['护卫'][1][0]
						numTF = [j - 1 >= 0, j + 1 <= 2]
						num_pos = [j - 1, j + 1]
						for k in range(2):
							if numTF[k]:
								self.LR[i][num_pos[k]].champion.defensive_attribute.armor += self.LR[i][j].flag.rela_flag['护卫'][1][1]

	# 召唤太阳圆盘
	def Tyyp(self,champion,Azir):
		end_flag = self.SolarDisk[1].Duration(self.SolarDisk[2])
		if end_flag:
			SolarDisk.__init__()
			SolarDisk.position = champion.position
			SolarDisk.pos_num = champion.pos_num
			SolarDisk.game = self
			SolarDisk.enemy = champion.enemy
			SolarDisk.champion.relatedness.element[1] = 4
			SolarDisk.champion.relatedness.profession[1] = 1
			self.LR[champion.position][champion.pos_num] = 	SolarDisk
			for i in range(3):
				SolarDisk.friend[i] = self.LR[SolarDisk.position][i]
			self.LR_ui[champion.position][champion.pos_num] = Champion_Interface(self.screen,SolarDisk,self)
			print('太阳圆盘升起')
			Azir.champion.skill.extra[2][1][2] = True
			self.SolarDisk[0] = False
	# 忍者buff
	def Ninja_buff(self,champion,buff_num):
		n = [0,buff_num]
		p = randint(0,2)
		for i in range(3):
			if champion.friend[p].flag.special_flag.chakra_flag and not champion.friend[p].flag.condition_flag.death_flag:
				champion.friend[p].flag.rela_flag['忍者'][3] = True
				print('%s获得忍者buff，%d' % (champion.friend[p].champion.name,buff_num))
				# 显示
				if champion.friend[p].champion.relatedness.profession[0] == '忍剑士':
					champion.friend[p].flag.rela_flag['忍剑士'][2][0] = True
				else:
					champion.friend[p].flag.rela_flag['忍者'][2][0] = True
				n[0] += 1
				if n[0] == n[1]:
					break
			p += 1
			if p == 3:
				p = 0
	# 机神合体
	def MechWarrior_Link(self,position):
		# 合体召唤机神盖伦
		if self.MechWarrior_flag[position][2][0].Duration(self.MechWarrior_flag[position][2][1]):
			print('合体')
			for i in range(3):
				if self.LR[position][i].champion.relatedness.element[0] == '银河机神':
					self.LR[position][i].flag.rela_flag['银河机神'][3][0] = True
			pos_num = 1
			if self.LR[position][1].champion.relatedness.element[0] != '银河机神':
				pos_num = 0
			# 存储合体位置原英雄
			self.MechWarrior_flag[position][4] = self.LR[position][pos_num]
			if self.MechWarrior_flag[position][1] == 2:
				champion = NormalGaren[position]
			elif self.MechWarrior_flag[position][1] == 3:
				champion = SuperGaren
			# 合体位置英雄换成盖伦
			champion.__init__()
			if self.MechWarrior_flag[position][1] == 3:
				SuperGaren.champion.name = 'SuperGaren'
				SuperGaren.champion.skill.describe = ['机神裁决：银河魔装机神盖伦召唤一','道毁灭冲击，对目标造成220点魔法伤','害，对周围敌人造成180点魔法伤害']
				SuperGaren.champion.hp.max_value = 1400
				SuperGaren.champion.hp.value = SuperGaren.champion.hp.max_value
				SuperGaren.champion.attack_attribute.attack_speed = 0.74
				SuperGaren.champion.attack_attribute.AD = 50
				SuperGaren.champion.defensive_attribute.armor = 45
				SuperGaren.champion.defensive_attribute.spell_resistance = 35
				SuperGaren.champion.skill.para = [220,160]
			champion.position = position
			champion.pos_num = pos_num
			champion.game = self
			champion.enemy = self.LR[position][pos_num].enemy
			champion.champion.relatedness.element[1] = 3
			champion.champion.relatedness.profession[1] = 2
			self.LR[position][pos_num] = champion
			for j in range(3):
				champion.friend[j] = self.LR[position][j]
			for j in range(3):
				if self.LR[position][j] != champion:
					self.LR[position][j].friend[champion.pos_num] = champion
			self.LR_ui[position][pos_num] = Champion_Interface(self.screen,champion,self)
			# 嘲讽
			numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
			num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
			for pos_num in range(3):
				if numTF[pos_num]:
					if not self.LR[~position+2][num_pos[pos_num]].flag.condition_flag.death_flag and not self.LR[~position+2][num_pos[pos_num]].flag.condition_flag.miss_flag[0] \
					and not self.LR[~position+2][num_pos[pos_num]].flag.condition_flag.buff_invincible_flag and not self.LR[~position+2][num_pos[pos_num]].flag.condition_flag.buff_unstoppable_flag:
						self.LR[~position+2][num_pos[pos_num]].enemy = champion
			self.MechWarrior_flag[position][3][0] = True
	# 显示ui
	def Show_ui(self,pos_mouse):
		for i in range(2):
			for j in range(3):
				if not self.LR[i][j].flag.rela_flag['银河机神'][3][0]:
					self.LR_ui[i][j].Draw(pos_mouse)

# 英雄参数
class Champion_basic_parameter(object):
	def __init__(self):
		self.number = 0										# 编号
		self.name = '测试英雄'                              	# 名字
		self.skill = Skill()          						# 技能系统			
		self.hp = HP()										# 生命值系统
		self.mp = MP()										# 法力值系统
		self.attack_attribute = Attack_attribute()			# 攻击参数
		self.defensive_attribute = Defensive_attribute()	# 防御参数
		self.hemophagia = 0 								# 生命偷取
		self.relatedness = Relatedness()					# 羁绊系统
# 	英雄参数_技能系统
class Skill(object):
	def __init__(self):
		self.name = '测试技能'											# 技能名称
		self.describe = '略'												# 技能描述
		self.active_skill = True										# 主动技能标志
		self.aoe = [False,False] 										# AOE技能标志|中心伤害法术暴击标志
		self.para = None 												# 技能参数
		self.comb = [False,0,0,False] 									# 是否为组合技能标志|下次技能编号|显示施法图标编号|第一段技能结束标志
		self.continuous = [False,False,False,False]      				# 持续施法技能标志|施法中标志|施法结束标志|被打断施法标志
		self.extra = [False,0,[[None,None,False] for _ in range(4)]] 	# 额外被动技能标志|额外被动技能数量|技能名|技能描述|技能触发标志
# 	英雄参数_生命值系统
class HP(object):
	def __init__(self):
		self.value = 500									# 生命值
		self.max_value = self.value 						# 最大生命值
		self.heal = 0                                       # 提供治疗总量
	# 生命回复
	def HP_restore(self,hp_restore_value,Achampion,B):              # A治疗B，Achampion为A.champion
		if not B.flag.condition_flag.death_flag and not B.flag.condition_flag.miss_flag[0]:
			if B.flag.weapon_flag.xsfq[0]:
				hp_restore_value *= (1 + B.flag.weapon_flag.xsfq[1])
			if B.flag.condition_flag.debuff_injury_flag: 			# 重伤效果
				hp_restore_value *= 0.3
			elif B.flag.condition_flag.debuff_burn_flag: 			# 灼烧效果
				hp_restore_value *= 0.6
			if (self.value + hp_restore_value) > self.max_value:
				# 过量治疗
				if B.flag.special_flag.extra_heal_flag:
					# 获得护盾
					shield_add = self.value + hp_restore_value - self.max_value
					B.condition.shield.Add_shield(B,shield_add,10)
					B.flag.special_flag.extra_heal_flag = False
				hp_restore_value = self.max_value - self.value
			self.value += hp_restore_value
			# 累计治疗量
			Achampion.hp.heal += hp_restore_value
	# 扣血、判断击杀
	def HP_reduce(self,damage_value,A,B):  				# A攻击B
		# 防止产生不可选取状态时被击杀的bug的临时补丁
		if B.flag.condition_flag.miss_flag[0]:
			damage_value = 0
		# 防止挑战期间被挑战目标以外敌人伤害的补丁
		if B.flag.special_flag.challenge[0] and A != B.flag.special_flag.challenge[1]:
			damage_value = 0
		if A.flag.weapon_flag.hazx[0] and damage_value > A.flag.weapon_flag.hazx[1]:
			A.flag.weapon_flag.hazx[3] = True
			A.flag.weapon_flag.hazx[4] += 1
			A.condition.injury.Add_injury(B, A.flag.weapon_flag.hazx[2]) 
		if B.champion.name == 'Annie' and tibbers.flag:
			# 计算提伯斯的生命值
			tibbers.Hp(B.champion.skill.para[2] * damage_value)
			damage_value *= (1 - B.champion.skill.para[2])
		# 计算B的生命值
		if B.condition.shield.value > damage_value: 	# 1：护盾值>伤害
			B.condition.shield.value -= damage_value
		else:
			if B.condition.shield.value > 0:						# 2：护盾值>0且<伤害
				B.champion.hp.value -= (damage_value - B.condition.shield.value)
				B.condition.shield.value = 0
			else:													# 3：无护盾
				B.champion.hp.value -= damage_value
		# 触发B的神圣救赎效果
		if B.flag.weapon_flag.ssjs[0] and B.flag.weapon_flag.ssjs[1] and not B.flag.weapon_flag.ssjs[4][0] and (B.champion.hp.value < B.flag.weapon_flag.ssjs[3] * B.champion.hp.max_value): 
			B.flag.weapon_flag.ssjs[4][0] = True																
		# 触发B的泰坦坚决效果
		elif B.flag.weapon_flag.ttjj[0]:
			B.weapon.Ttjj(B)
		# 触发B的巨石板甲效果
		elif B.flag.weapon_flag.jsbj[0]:
			B.weapon.Jsbj(B)
		# 触发B的圣银胸甲效果
		elif B.flag.weapon_flag.syxj[0] and not B.flag.weapon_flag.syxj[3] and (B.champion.hp.value < B.flag.weapon_flag.syxj[1] * B.champion.hp.max_value):
			B.champion.defensive_attribute.armor *= (1 + B.flag.weapon_flag.syxj[2])
			B.champion.defensive_attribute.spell_resistance *= (1 + B.flag.weapon_flag.syxj[2])
			B.flag.weapon_flag.syxj[3] = True
		# 触发加里奥的巨像重击
		if B.champion.name == 'Galio':
			B.Thump()
		# 触发薇恩的终极时刻
		elif B.champion.name == 'Vayne':
			if B.champion.hp.value <= (B.champion.hp.max_value * B.champion.skill.para[1][0]) and not B.champion.skill.para[1][5]:
				B.Ultimate()
		# 触发布里兹法力屏障效果
		elif B.champion.name == 'Blitz':
			if not B.champion.skill.para[2][0] and (B.champion.hp.value < B.champion.hp.max_value * B.champion.skill.para[2][1]):
				B.Barrier()
		# 触发菲兹的古灵精怪
		elif B.champion.name == 'Fizz' and version[0] == 3:
			if not B.flag.special_flag.odd[1] and (B.champion.hp.value < B.champion.skill.para[4]):
				B.Odd(0)
		# 触发羊灵生息
		if B.champion.hp.value <= (B.champion.hp.max_value * B.flag.special_flag.bless_land[1]):
			for i in range(3):
				if B.friend[i].champion.name == 'Kindred':
					Kindred = B.friend[i]
					if not Kindred.flag.condition_flag.death_flag and not Kindred.flag.condition_flag.miss_flag[0]:
						if B == Kindred:
							if not Kindred.champion.skill.para[3]:
								Kindred.Ylsx()
						else:	
							if B.flag.special_flag.dead_area[0] == Kindred.flag.special_flag.dead_area[0]:
								if not Kindred.champion.skill.para[3]:
									Kindred.Ylsx()
		# 触发B钢铁羁绊
		if B.flag.rela_flag['钢铁'][0]:
			if (B.champion.hp.value < rela_dic['钢铁'][1][3] * B.champion.hp.max_value) and B.flag.condition_flag.buff_iron_flag[1]:
				B.condition.iron.Add_iron(B,B.flag.rela_flag['钢铁'][1])
				B.flag.rela_flag['钢铁'][2] = [True,B.flag.rela_flag['钢铁'][1]]
		# 触发A掠食者羁绊，钢铁状态免疫斩杀
		if A.flag.rela_flag['掠食者'][0] and not B.flag.condition_flag.buff_iron_flag[0]:
			if B.champion.hp.value < A.flag.rela_flag['掠食者'][1] * B.champion.hp.max_value:
				B.champion.hp.value = 0
				A.flag.rela_flag['掠食者'][2][0] = True
		# 触发赐福之地效果
		if B.flag.special_flag.bless_land[0] and B.champion.hp.value <= B.champion.hp.max_value * B.flag.special_flag.bless_land[1]:
			B.champion.hp.value = B.champion.hp.max_value * B.flag.special_flag.bless_land[1]
		# B濒死
		if B.champion.hp.value < 1:
			B.champion.hp.value = 0
			# 触发巫师法帽效果
			if B.flag.weapon_flag.wsfm[2][0]:
				B.weapon.Wsfm(B)
			# 触发守护天使效果
			elif B.flag.weapon_flag.shts[1]:
				B.weapon.Shts(B)
			# 触发弗拉基米尔血红之池
			elif B.champion.name == 'Vladimir' and not B.flag.special_flag.blood_pool[1]:
				B.Blood()
			elif not B.flag.condition_flag.miss_flag[0]:
				B.flag.condition_flag.death_flag = True 	# B死亡
				A.flag.special_flag.kill[0] = True          # A造成击杀
				# 触发A的荣光凯旋效果
				if A.flag.weapon_flag.rgkx[0]:
					A.weapon.Rgkx(A)
				for i in range(3):
					if A.flag.special_flag.kill[i+1] == None:
						A.flag.special_flag.kill[i+1] = B
						A.flag.special_flag.kill[4] += 1
						break
				# 打开虚空之门
				if B.flag.weapon_flag.xkzm[0]:
					B.weapon.Xkzm(B)
# 	英雄参数_法力值系统
class MP(object):
	def __init__(self):
		self.value = 0                    					# 初始法力值
		self.max_value = 150              					# 最大法力值
		self.basic_MP_restore = 10        					# 普攻基础回蓝
		self.max_MP_restore = 45          					# 受伤回蓝最大值
	# 回蓝计算
	def Calculation(self,champion,mp_restore_value):
		if champion.flag.condition_flag.debuff_silence_flag or champion.champion.skill.continuous[1]:
			mp_restore_value = 0
		if champion.flag.condition_flag.debuff_poisoning_flag[0]:	# 中毒效果
			if champion.flag.condition_flag.debuff_poisoning_flag[1] == 0:
				mp_restore_value *= (1 - rela_dic['剧毒'][1][0])
			else:
				mp_restore_value *= (1 - rela_dic['剧毒'][1][1])
		if champion.champion.name == 'Jinx':
			if champion.champion.attack_attribute.attack_speed >= champion.champion.skill.para[5]:
				mp_restore_value = 0
		self.value += mp_restore_value
		if self.value > self.max_value:
			self.value = self.max_value
	# 回蓝机制1(普攻回蓝并令敌人回蓝)
	def MP_restore_1(self,flag,champion,enemy):
		# 普攻回蓝
		if flag.damage_calculation_flag.normal_attack: 		# 普攻造成伤害才回蓝
			value_MP_restore_1 = randint(int(self.basic_MP_restore/2), self.basic_MP_restore)
			if flag.weapon_flag.sjzm[1] and not champion.flag.special_flag.chakra_flag:    # 触发朔极之矛的效果
				value_MP_restore_1 += int(flag.weapon_flag.sjzm[2] * self.max_value)
			self.Calculation(champion,value_MP_restore_1)
			# 敌人被打回蓝_普攻
			value_MP_restore_2_1 = champion.champion.attack_attribute.normal_attack_damage.total_damage/5
			if value_MP_restore_2_1 > self.max_MP_restore:
				value_MP_restore_2_1 = self.max_MP_restore
			enemy.champion.mp.Calculation(enemy,value_MP_restore_2_1)	
	# 回蓝机制2(技能伤害令敌人回蓝)
	def MP_restore_2(self,flag,champion,enemy,mode):
		# 敌人被打回蓝_技能伤害
		if mode == 0:
			if flag.damage_calculation_flag.spell_attack:
				value_MP_restore_2_2 = champion.champion.attack_attribute.spell_attack_damage.total_damage/5
				if value_MP_restore_2_2 > self.max_MP_restore:
					value_MP_restore_2_2 = self.max_MP_restore
				enemy.champion.mp.Calculation(enemy,value_MP_restore_2_2)
		# 特殊情况：不属于普攻但计算方式为普攻伤害
		elif mode == 1:
			if flag.damage_calculation_flag.normal_attack:
				value_MP_restore_2_3 = champion.champion.attack_attribute.normal_attack_damage.total_damage/5
				if value_MP_restore_2_3 > self.max_MP_restore:
					value_MP_restore_2_3 = self.max_MP_restore
				enemy.champion.mp.Calculation(enemy,value_MP_restore_2_3)
# 	英雄参数_攻击参数
class Attack_attribute(object):
	def __init__(self):
		# 普攻相关
		self.attack_speed = 1								# 攻速
		self.AD = 50										# 物攻
		self.armor_penetration = 0     						# 穿甲
		self.crit_mechanism = Crit()						# 暴击机制
		self.normal_attack = Normalattack(self.AD)          # 普攻伤害成分
		self.normal_attack_orig = Normalattack(self.AD) 	# 普攻伤害成分原值
		self.normal_attack_time_count = 0					# 普攻间隔时间计数值
		self.normal_attack_damage = Damage() 				# 普攻造成伤害成分
		self.attack_count = 0 								# 普攻计数
		# 技能相关
		self.spell_power = 1								# 法强
		self.spell_resistance_penetration = 0               # 法穿
		self.spell_attack = Damage()                 		# 技能伤害成分
		self.spell_attack_damage = Damage()   				# 技能造成伤害成分
		self.all_damage = All_damage()                     	# 累计造成伤害
#		英雄参数_攻击参数_暴击机制
class Crit(object):
	def __init__(self):
		self.crit = 0.25									# 暴击率
		self.crit_multiple = 1.5							# 暴击伤害倍数
		self.crit_count = 0                                	# 暴击次数
		self.crit_flag = False  							# 暴击标志
	# 暴击判断
	def Crit_judg(self):
		# 用随机数判断暴击
		if randint(0,99) < self.crit * 100:
			self.crit_count += 1
			return True
		else:
			return False
	# 增加暴击
	def Add_crit(self,crit_value):
		self.crit += crit_value
		if self.crit > 1:
			self.crit = 1
# 		英雄参数_攻击参数_伤害成分
class Damage(object):
	def __init__(self):
		self.physical_damage = 0
		self.spell_damage = 0
		self.real_damage = 0
		self.total_damage = 0
	# 计算造成总伤害
	def Total_damage_calculation(self):
		self.total_damage = self.physical_damage + self.spell_damage + self.real_damage
# 		英雄参数_攻击参数_普通攻击成分
class Normalattack(Damage):
	def __init__(self,AD):
		super().__init__()
		self.physical_damage = AD
# 		英雄参数_攻击参数_累计造成伤害
class All_damage(Damage):
	def __init__(self):
		super().__init__()
	def Calculation(self,damage):
		self.physical_damage += damage.physical_damage
		self.spell_damage += damage.spell_damage
		self.real_damage += damage.real_damage
		self.Total_damage_calculation()
# 	英雄参数_防御参数
class Defensive_attribute(object):
	def __init__(self):
		self.armor = 40										# 护甲
		self.spell_resistance = 20   						# 魔抗
		self.dodge_mechanism = Dodge()						# 闪避机制
		self.tenacity = 1                                 	# 韧性
		self.tenacity_max = 4
	# 增加韧性
	def Add_tenacity(self,tenacity_value):
		self.tenacity += tenacity_value
		if self.tenacity > self.tenacity_max:
			self.tenacity = self.tenacity_max
#		英雄参数_防御参数_闪避机制
class Dodge(object):
	def __init__(self):
		self.dodge = 0.05                                 	# 闪避率
		self.dodge_count = 0                           		# 闪避次数
		self.all_dodge = [False,0,False]					# 反击风暴完全闪避标志|反击风暴期间闪避普攻次数|鬼影重重/魂佑完全闪避标志
	# 闪避判断(敌方)
	def Dodge_judg(self,enemy):
		# 若处于完全闪避情况
		#	反击风暴
		if enemy.champion.defensive_attribute.dodge_mechanism.all_dodge[0]:
			enemy.champion.defensive_attribute.dodge_mechanism.dodge_count += 1
			enemy.champion.defensive_attribute.dodge_mechanism.all_dodge[1] += 1
			return 1
		#	鬼影重重/魂佑
		elif enemy.champion.defensive_attribute.dodge_mechanism.all_dodge[2]:
			enemy.champion.defensive_attribute.dodge_mechanism.dodge_count += 1
			# 触发慎的忍法！气合盾效果
			if enemy.champion.name == 'Shen':
				enemy.Ninja_shield()
			return 1
		# 用随机数判断闪避
		elif randint(0,99) < enemy.champion.defensive_attribute.dodge_mechanism.dodge * 100:
			enemy.champion.defensive_attribute.dodge_mechanism.dodge_count += 1
			# 触发慎的忍法！气合盾效果
			if enemy.champion.name == 'Shen':
				enemy.Ninja_shield()
			# 被压制时不可闪避普攻，但完全闪避状态可以闪避
			if not enemy.flag.condition_flag.suppress[0]:
				return 1
			else:
				return 0
		else:
			return 0
	def Add_dodge(self,dodge_value):
		self.dodge += dodge_value
		# 最大闪避率为90%
		if self.dodge > 0.9:
			self.dodge = 0.9
#	英雄参数_羁绊系统
class Relatedness(object):
	def __init__(self):
		self.element = ['None',0]									# 元素
		self.profession = ['None',0]								# 职业
		self.extra = ['None',0] 									# 额外
		self.thunder_number = 0 									# 触发雷霆羁绊计数值
		# 海洋羁绊效果
	def Sea(self,game,position):
		end_flag = game.sea_flag[position][2].Duration(rela_dic['海洋'][1][3] * 3)
		if end_flag:
			mp_restore_value = rela_dic['海洋'][1][game.sea_flag[position][1]]
			for i in range(3):
				if game.LR[position][i].flag.rela_flag['海洋'][0]:
					game.LR[position][i].flag.rela_flag['海洋'][2][0] = True
				if not game.LR[position][i].flag.condition_flag.death_flag and not game.LR[position][i].flag.special_flag.chakra_flag:
					game.LR[position][i].champion.mp.Calculation(game.LR[position][i],mp_restore_value)
	# 森林羁绊效果
	def Forest(self,champion):
		champion.flag.rela_flag['森林'][3] += 1
		if champion.flag.rela_flag['森林'][3] >= (rela_dic['森林'][1][3] * 100 / time_correction[0]):
			hp_restore_value = champion.flag.rela_flag['森林'][1]
			champion.champion.hp.HP_restore(hp_restore_value,champion.champion,champion)
			champion.flag.rela_flag['森林'][3] = 0
			champion.flag.rela_flag['森林'][2][0] = True
	# 光羁绊效果
	def Light(self,champion):
		# 光羁绊——光之祭献
		if champion.flag.rela_flag['光'][0] and not champion.flag.special_flag.dead_area[0]:
			for i in range(3):
				if champion.friend[i] != champion and not champion.friend[i].flag.condition_flag.death_flag and not champion.friend[i].flag.condition_flag.miss_flag[0]\
				and not champion.friend[i].flag.special_flag.dead_area[0]:
					# 治疗生命值
					value_treatment = champion.flag.rela_flag['光'][1][0]*champion.friend[i].champion.hp.max_value
					champion.friend[i].champion.hp.HP_restore(value_treatment, champion.champion, champion.friend[i])
					if champion.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
						champion.condition.fervor.Add_fervor(champion.friend[i],champion.flag.weapon_flag.crxl[2][2])
						champion.flag.weapon_flag.crxl[3] = True
					# 加攻速
					champion.friend[i].champion.attack_attribute.attack_speed *= (1 + champion.flag.rela_flag['光'][1][1])
					champion.friend[i].flag.special_flag.effect['光之祭献'][0] = True
	# 水晶羁绊效果
	def Crystal(self,enemy,total_damage):
		if total_damage > enemy.flag.rela_flag['水晶'][1]:
			total_damage = enemy.flag.rela_flag['水晶'][1]
			enemy.flag.rela_flag['水晶'][2][0] = True
		return total_damage
	# 狂战士羁绊效果(以及格雷福斯被动效果)
	def Berserker(self,champion):
		if not champion.flag.special_flag.dead_area[0]:
			enemy = champion.enemy
			num_pos = [champion.enemy.pos_num - 1, champion.enemy.pos_num + 1]
			numTF = [(num_pos[0] >= 0 and not champion.game.LR[~champion.position+2][num_pos[0]].flag.condition_flag.death_flag and not champion.game.LR[~champion.position+2][num_pos[0]].flag.condition_flag.miss_flag[0])\
			and not champion.game.LR[~champion.position+2][num_pos[0]].flag.special_flag.dead_area[0], (num_pos[1] <= 2 and not champion.game.LR[~champion.position+2][num_pos[1]].flag.condition_flag.death_flag \
				and not champion.game.LR[~champion.position+2][num_pos[1]].flag.condition_flag.miss_flag[0]) and not champion.game.LR[~champion.position+2][num_pos[1]].flag.special_flag.dead_area[0]]
			# 顺劈溅射伤害标志
			champion.flag.rela_flag['狂战士'][3] = True
			# 伤害计算
			for i in range(2):
				if numTF[i]:
					# 判断目标
					champion.enemy = champion.game.LR[~champion.position+2][num_pos[i]]
					dodge_flag = False
					if champion.champion.name == 'Graves':
						# 判断闪避，格雷福斯的被动散弹是可以被闪避的，狂战士的溅射伤害是不会被闪避的
						dodge_flag = champion.champion.defensive_attribute.dodge_mechanism.Dodge_judg(champion.enemy) \
						and (not champion.enemy.flag.condition_flag.debuff_dizz_flag) and (not champion.enemy.flag.condition_flag.debuff_frozen_flag)
						if champion.flag.weapon_flag.jshp[0]:  					# 触发疾射火炮效果(但对面闪避判断记为成功)
							dodge_flag = False
						if dodge_flag:
							if champion.enemy.flag.weapon_flag.fshf[0]: 			# 触发飞升护符效果(敌人)
								champion.weapon.Fshf(champion)
							elif champion.enemy.flag.weapon_flag.qfzl[0]: 			# 触发清风之灵效果(敌人)
								champion.weapon.Qfzl(champion)
							elif champion.enemy.flag.weapon_flag.bmhs[0]:			# 触发冰脉护手效果(敌人)
								champion.weapon.Bmhs(champion)
					# 复制普攻伤害原值
					champion.champion.attack_attribute.normal_attack.physical_damage = champion.champion.attack_attribute.normal_attack_orig.physical_damage
					champion.champion.attack_attribute.normal_attack.spell_damage = champion.champion.attack_attribute.normal_attack_orig.spell_damage
					champion.champion.attack_attribute.normal_attack.real_damage = champion.champion.attack_attribute.normal_attack_orig.real_damage
					if not dodge_flag:
						champion.Normal_attack_damage_calculation()
						# 计算敌人回蓝
						champion.champion.mp.MP_restore_2(champion.flag, champion, champion.enemy, 1)
			champion.flag.rela_flag['狂战士'][3] = False
			champion.enemy = enemy
		if champion.champion.name != 'Graves':
			champion.flag.rela_flag['狂战士'][2][0] = True
		champion.flag.rela_flag['狂战士'][4] = False
	# 游侠羁绊效果
	def Ranger(self,champion):
		# 第一阶段：等待阶段
		if champion.flag.rela_flag['游侠'][3][0] == 1:
			end_flag1 = champion.flag.rela_flag['游侠'][3][1].Duration(champion.flag.rela_flag['游侠'][1])
			if end_flag1:
				champion.flag.rela_flag['游侠'][3][0] = 2
				# 攻速翻倍
				champion.champion.attack_attribute.attack_speed *= 2
				champion.flag.rela_flag['游侠'][2][0] = True
		# 第二阶段：攻速翻倍阶段
		else:
			end_flag2 = champion.flag.rela_flag['游侠'][3][2].Duration(rela_dic['游侠'][1][2])
			if end_flag2:
				champion.flag.rela_flag['游侠'][3][0] = 1
				# 攻速复原
				champion.champion.attack_attribute.attack_speed /= 2
	# 极地羁绊效果
	def Ice(self,champion):
		if randint(0,99) < 100 * champion.flag.rela_flag['极地'][1]:
			champion.flag.rela_flag['极地'][2][0] = True 													# 显示触发极地羁绊
			frozen_time = rela_dic['极地'][1][3] / champion.enemy.champion.defensive_attribute.tenacity
			if champion.flag.weapon_flag.jdzc[0]: 												     		# 触发极地战锤效果
				frozen_time += champion.flag.weapon_flag.jdzc[1]
				champion.flag.weapon_flag.jdzc[2] = True
				champion.flag.weapon_flag.jdzc[3] += 1
			if champion.enemy.flag.condition_flag.debuff_burn_flag:
				champion.enemy.condition.burn.Clean(champion.enemy.flag)
				print('冰消火')
			champion.condition.frozen.Add_frozen(champion.enemy,frozen_time)
	# 地狱火羁绊效果
	def Fire(self,champion):
		if randint(0,99) < 100 * rela_dic['地狱火'][1][4]:
			if champion.champion.relatedness.element[0] == '黯焰':
				champion.flag.rela_flag['黯焰'][2][0] = True
			else:
				champion.flag.rela_flag['地狱火'][2][0] = True 									# 显示触发地狱火羁绊
			champion.enemy.condition.burn.source = champion
			if champion.enemy.flag.condition_flag.debuff_frozen_flag:
				champion.enemy.condition.frozen.Clean(champion.enemy.flag,champion.enemy)
				print('火消冰')
			champion.condition.burn.Add_burn(champion.enemy,rela_dic['地狱火'][1][3])
	# 银月羁绊效果
	def Moon(self,game,position):
		if game.moon_flag[position][3] < rela_dic['银月'][1][3]:
			end_flag = game.moon_flag[position][2].Duration(rela_dic['银月'][1][2] * 3)
			if end_flag:
				game.moon_flag[position][3] += 1
				for i in range(3):
					if game.LR[position][i].flag.rela_flag['银月'][0]:
						game.LR[position][i].flag.rela_flag['银月'][2][0] = True
					if not game.LR[position][i].flag.condition_flag.death_flag:
						game.LR[position][i].champion.attack_attribute.crit_mechanism.Add_crit(rela_dic['银月'][1][game.moon_flag[position][1]][0])
						game.LR[position][i].champion.attack_attribute.crit_mechanism.crit_multiple += rela_dic['银月'][1][game.moon_flag[position][1]][1]
						game.LR[position][i].champion.attack_attribute.spell_power += rela_dic['银月'][1][game.moon_flag[position][1]][2]
						game.LR[position][i].flag.special_flag.effect['月光'][0] = True
	# 雷霆羁绊效果
	def Thunder(self,champion):
		# 判断落雷
		if randint(0,99) < (champion.flag.rela_flag['雷霆'][1][0] * 100):
			# 显示触发雷霆羁绊
			champion.flag.rela_flag['雷霆'][2][0] = True
			champion.champion.relatedness.thunder_number += 1
			# 判断目标：优先攻击感电目标，否则随机
			enemy = None
			for i in range(3):
				if not champion.game.LR[~champion.position+2][i].flag.condition_flag.death_flag and not champion.game.LR[~champion.position+2][i].flag.condition_flag.miss_flag[0] \
				and champion.game.LR[~champion.position+2][i].flag.condition_flag.debuff_electrification_flag:
					enemy =  champion.game.LR[~champion.position+2][i]
					break
			if enemy == None:
				p = randint(0,2)
				for _ in range(3):
					if not champion.game.LR[~champion.position+2][p].flag.condition_flag.death_flag and not champion.game.LR[~champion.position+2][p].flag.condition_flag.miss_flag[0]:
						enemy = champion.game.LR[~champion.position+2][p]
						break
					else:
						p += 1
						if p == 3:
							p = 0 
			if not enemy == None:
				# 计算伤害
				# 判断敌人的魔法护盾(伏击之爪无法格挡)
				if enemy.flag.condition_flag.buff_magic_shield_flag:
					enemy.flag.condition_flag.buff_magic_shield_flag = False
				elif enemy.flag.condition_flag.buff_invincible_flag: # 目标处于无敌状态则只显示落雷不造成伤害
					enemy.flag.special_flag.effect['落雷'][0] = True
				else:
					if enemy.flag.weapon_flag.symj[1]: 											# 触发深渊面具效果
						enemy.flag.weapon_flag.symj[2] = 1 + enemy.flag.weapon_flag.symj[3]
					thunder_damage = (champion.flag.rela_flag['雷霆'][1][1] * (100 / (100 + (enemy.champion.defensive_attribute.spell_resistance \
						* ((1 - champion.champion.attack_attribute.spell_resistance_penetration/100)))))) * enemy.flag.weapon_flag.symj[2] * enemy.condition.matigation.value * enemy.condition.iron.value
					if enemy.flag.weapon_flag.jlzy[0]: 											# 触发敌人的巨龙之牙效果
						thunder_damage *= (1 - enemy.flag.weapon_flag.jlzy[1])
					# 触发泰坦坚决效果
					if champion.flag.weapon_flag.ttjj[0]:
						thunder_damage *= champion.flag.weapon_flag.ttjj[2][0]
					# 感电状态伤害增幅
					if enemy.flag.condition_flag.debuff_electrification_flag:
						thunder_damage *= enemy.condition.electrification.amplification
					# 扣血、击杀判断
					enemy.champion.hp.HP_reduce(thunder_damage,champion,enemy)
					# 触发凯南的雷缚印效果
					if champion.champion.name == 'Kennen':
						champion.Thunder_sign(enemy)
					# 触发科技枪刃效果
					if champion.flag.weapon_flag.kjqr[0]: 								
						hp_restore_value = champion.flag.weapon_flag.kjqr[1] * thunder_damage
						champion.champion.hp.HP_restore(hp_restore_value,champion.champion,champion)
					# 累计造成伤害
					champion.champion.attack_attribute.all_damage.spell_damage += thunder_damage
					champion.champion.attack_attribute.all_damage.Total_damage_calculation()
					enemy.flag.special_flag.effect['落雷'][0] = True
	# 枪手羁绊效果
	def Marksman(self,champion):
		temp_enemy = champion.enemy
		# 额外攻击标志
		champion.flag.rela_flag['枪手'][3] = True
		# 随机敌人
		p = randint(0,2)
		enemy = champion.game.LR[~champion.position+2]
		# 攻击次数
		n = 0
		# 伤害计算
		for i in range(3):
			# 判断目标
			if enemy[p] != temp_enemy and not enemy[p].flag.condition_flag.death_flag and not enemy[p].flag.condition_flag.miss_flag[0]:
				champion.enemy = enemy[p]
				# 判断闪避，枪手的额外攻击是计算闪避机制的
				dodge_flag = champion.champion.defensive_attribute.dodge_mechanism.Dodge_judg(champion.enemy) \
				and (not champion.enemy.flag.condition_flag.debuff_dizz_flag) and (not champion.enemy.flag.condition_flag.debuff_frozen_flag)
				if champion.flag.weapon_flag.jshp[0]:  					# 触发疾射火炮效果(但对面闪避判断记为成功)
					dodge_flag = False
				if dodge_flag:
					if champion.enemy.flag.weapon_flag.fshf[0]: 			# 触发飞升护符效果(敌人)
						champion.weapon.Fshf(champion)
					elif champion.enemy.flag.weapon_flag.qfzl[0]: 			# 触发清风之灵效果(敌人)
						champion.weapon.Qfzl(champion)
					elif champion.enemy.flag.weapon_flag.bmhs[0]:			# 触发冰脉护手效果(敌人)
						champion.weapon.Bmhs(champion)
				# 复制普攻伤害原值
				champion.champion.attack_attribute.normal_attack.physical_damage = champion.champion.attack_attribute.normal_attack_orig.physical_damage
				champion.champion.attack_attribute.normal_attack.spell_damage = champion.champion.attack_attribute.normal_attack_orig.spell_damage
				champion.champion.attack_attribute.normal_attack.real_damage = champion.champion.attack_attribute.normal_attack_orig.real_damage
				if not dodge_flag:
					champion.Normal_attack_damage_calculation()
					# 计算敌人回蓝
					champion.champion.mp.MP_restore_2(champion.flag, champion, champion.enemy, 1)
				# 记录弹道
				champion.flag.rela_flag['枪手'][5][n] = champion.enemy.pos_num
				# 攻击次数计数
				n += 1
				if n == champion.flag.rela_flag['枪手'][1][1]:
					break
				p += 1
				if p == 3:
					p = 0
			else:
				p += 1
				if p == 3:
					p = 0
		champion.flag.rela_flag['枪手'][3] = False
		champion.enemy = temp_enemy
		if n > 0:
			champion.flag.rela_flag['枪手'][2][0] = True
		champion.flag.rela_flag['枪手'][4] = False
	# 影羁绊效果
	def Shadow(self,champion,mode):
		# mode = 0为普攻伤害
		if mode == 0:
			champion.champion.attack_attribute.normal_attack.real_damage += champion.champion.attack_attribute.normal_attack.physical_damage * champion.flag.rela_flag['影'][1]
			champion.champion.attack_attribute.normal_attack.physical_damage *= (1 - champion.flag.rela_flag['影'][1])
			champion.champion.attack_attribute.normal_attack.real_damage += champion.champion.attack_attribute.normal_attack.spell_damage * champion.flag.rela_flag['影'][1]
			champion.champion.attack_attribute.normal_attack.spell_damage *= (1 - champion.flag.rela_flag['影'][1])
		# mode = 1为技能伤害
		else:
			champion.champion.attack_attribute.spell_attack.real_damage += champion.champion.attack_attribute.spell_attack.physical_damage * champion.flag.rela_flag['影'][1]
			champion.champion.attack_attribute.spell_attack.physical_damage *= (1 - champion.flag.rela_flag['影'][1])
			champion.champion.attack_attribute.spell_attack.real_damage += champion.champion.attack_attribute.spell_attack.spell_damage * champion.flag.rela_flag['影'][1]
			champion.champion.attack_attribute.spell_attack.spell_damage *= (1 - champion.flag.rela_flag['影'][1])
	# 剑士羁绊触发判定
	def Swordsman1(self,champion):
		if not champion.flag.rela_flag['剑士'][3]:
			if (randint(0,99) < int(rela_dic['剑士'][1][2] * 100)):
				# 攻速提升
				if champion.champion.name == 'Jhin':
					champion.As2cr(2)
				else:
					champion.champion.attack_attribute.attack_speed *= rela_dic['剑士'][1][3]
				champion.flag.rela_flag['剑士'][3] = True
	# 剑士羁绊消耗记录
	def Swordsman2(self,champion):
		if champion.flag.rela_flag['剑士'][3]:
			# 计数
			#	易双重打击不消耗剑士羁绊效果
			if champion.champion.name == 'Yi':
				if not champion.champion.skill.para[5][0]:
					champion.flag.rela_flag['剑士'][4] += 1
			else:
				champion.flag.rela_flag['剑士'][4] += 1
			if champion.flag.rela_flag['剑士'][4] >= champion.flag.rela_flag['剑士'][1]:
				champion.flag.rela_flag['剑士'][4] = 0
				# 攻速恢复
				if champion.champion.name == 'Jhin':
					champion.As2cr(1 / 2)
				else:
					champion.champion.attack_attribute.attack_speed /= rela_dic['剑士'][1][3]
				champion.flag.rela_flag['剑士'][3] = False
	# 爆破专家羁绊效果
	def Blast(self,champion):
		# 眩晕
		if not champion.enemy.flag.condition_flag.buff_invincible_flag and not champion.enemy.flag.condition_flag.buff_unstoppable_flag\
		 and not (champion.enemy.flag.special_flag.challenge[0] and champion != champion.enemy.flag.special_flag.challenge[1]):
			dizz_time = champion.flag.rela_flag['爆破专家'][1] / champion.enemy.champion.defensive_attribute.tenacity
			champion.condition.dizz.Add_dizz(champion.enemy,dizz_time)
			# 触发爆破炸弹效果
			if champion.flag.weapon_flag.bpzd[0]:
				champion.weapon.Bpzd(champion,champion.enemy)
		# 显示
		champion.flag.rela_flag['爆破专家'][2][0] = True
	# 奥德赛羁绊效果
	def Odyssey(self,game,position,mode,champion):
		# mode==0:开局;mode==1:中途转职(护盾收益不补偿)
		if mode == 1:
			numTF = [True,champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
			num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
			for i in range(3):
				if numTF[i]:
					if champion.game.LR[champion.position][num_pos[i]].champion.relatedness.element[0] == '奥德赛' or champion.game.LR[champion.position][num_pos[i]].champion.relatedness.extra[0] == '奥德赛'\
					and not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag and not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
						# 护盾
						champion.condition.shield.Add_shield(champion.game.LR[champion.position][num_pos[i]],champion.flag.rela_flag['奥德赛'][1][0],rela_dic['奥德赛'][1][2])
			# 增伤重置
			for i in range(3):
				game.LR[position][i].flag.rela_flag['奥德赛'][3] = 1
		for i in range(3):
			if game.LR[position][i].champion.relatedness.element[0] == '奥德赛' or game.LR[position][i].champion.relatedness.extra[0] == '奥德赛'\
			and not game.LR[position][i].flag.condition_flag.death_flag and not game.LR[position][i].flag.condition_flag.miss_flag[0]:
				champion = game.LR[position][i]
				# 显示
				champion.flag.rela_flag['奥德赛'][2][0] = True
				numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
				num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num +1]
				for i in range(3):
					if numTF[i]:
						if champion.game.LR[champion.position][num_pos[i]].champion.relatedness.element[0] == '奥德赛' or champion.game.LR[champion.position][num_pos[i]].champion.relatedness.extra[0] == '奥德赛' \
						and not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag and not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
							# 护盾
							if mode == 0:
								champion.condition.shield.Add_shield(champion.game.LR[champion.position][num_pos[i]],champion.flag.rela_flag['奥德赛'][1][0],rela_dic['奥德赛'][1][2])
							# 增伤
							champion.game.LR[champion.position][num_pos[i]].flag.rela_flag['奥德赛'][3] += champion.game.LR[champion.position][num_pos[i]].flag.rela_flag['奥德赛'][1][1]
	# 星之守护者羁绊效果
	def Star(self,champion):
		champion.flag.rela_flag['星之守护者'][2][0] = True
		for i in range(3):
			if (champion.friend[i].champion.relatedness.element[0] == '星之守护者' or champion.friend[i].champion.relatedness.extra[0] == '星之守护者') and \
			not champion.friend[i].flag.condition_flag.death_flag and champion.friend[i] != champion:
				champion.friend[i].champion.mp.Calculation(champion.friend[i],champion.flag.rela_flag['星之守护者'][1])
	# 未来战士羁绊效果
	def Future(self,game,position):
		end_flag = game.future_flag[position][2].Duration(rela_dic['未来战士'][1][2] * 3)
		if end_flag:
			for i in range(3):
				if game.LR[position][i].flag.rela_flag['未来战士'][0]:
					game.LR[position][i].flag.rela_flag['未来战士'][2][0] = True
				if not game.LR[position][i].flag.condition_flag.death_flag:
					# 攻速提升
					if game.LR[position][i].champion.name == 'Jhin':
						game.LR[position][i].As2cr((1 + rela_dic['未来战士'][1][game.future_flag[position][1]]))
					else:
						game.LR[position][i].champion.attack_attribute.attack_speed *= (1 + rela_dic['未来战士'][1][game.future_flag[position][1]])
					game.LR[position][i].flag.special_flag.effect['时间'][0] = True
	# 暗星羁绊效果
	def Death(self,champion):
		# 死亡祭献
		for i in range(2):
			for j in range(3):
				if champion.game.LR[i][j].flag.rela_flag['暗星'][0] and not champion.game.LR[i][j].flag.condition_flag.death_flag:
					champion.game.LR[i][j].flag.special_flag.effect['死亡祭献'][0] = True
					champion.game.LR[i][j].flag.rela_flag['暗星'][2][0] = True
					champion.game.LR[i][j].flag.rela_flag['暗星'][3] += 1
					if (champion.champion.relatedness.element[0] == '暗星' or champion.champion.relatedness.extra[0] == '暗星') and champion.position == i:
						champion.game.LR[i][j].flag.rela_flag['暗星'][3] += 1

# 标志
class Flag(object):
	def __init__(self):
		self.move_flag = Move_flag()                           	# 行为标志
		self.condition_flag = Condition_flag()                 	# 状态标志
		self.special_flag = Special_flag()           	      	# 特殊标志
		self.damage_calculation_flag = Damage_calculation_flag()# 伤害计算标志
		self.weapon_flag = Weapon_flag()						# 武器标志
		# 羁绊标志
		self.rela_flag = {'光' : [False,None,[False,1]],'沙漠' : [False,None,[False,0]], '极地' : [False,None,[False,1]], \
		'森林' : [False,None,[False,1],0,False], '水晶' : [False,None,[False,1]], '海洋' : [False,None,[False,1]], \
		'钢铁' : [False,None,[False,3]], '游侠' : [False,None,[False,3],[1,Time_count(),Time_count()]], \
		'掠食者' : [False,None,[False,1.5]], '狂战士' : [False,None,[False,0.7],False,False], '秘术师' : [False,None,[False,0]], \
		'守护神' : [False,None,[False,0]], '刺客' : [False,None,[False,0]], '法师' : [False,None,[False,0]], \
		'大元素使' : [False,None,[False,0]], '地狱火' : [False,None,[False,1.5]], '影' : [False,None,[False,0]], \
		'黯焰' : [False,None,[False,1.5]], '恕瑞玛之皇' : [False,None,[False,0]],'太阳圆盘' : [False,None,[False,0]], \
		'斗士' : [False,None,[False,0]], '银月' : [False,None,[False,1]], '剧毒' : [False,None,[False,1]], \
		'剑士' : [False,None,[False,0],False,0], '枪手' : [False,None,[False,0.7],False,False,[None,None]], '云霄' : [False,None,[False,0]], \
		'雷霆' : [False,None,[False,0.7]], '忍者' : [False,None,[False,0],False], '忍剑士' : [False,None,[False,0],False], \
		'银河机神' : [False,None,[False,0.8],[False,False]],'奥德赛' : [False,None,[False,1],1],'未来战士' : [False,None,[False,0.7]],'星神' : [False,None,[False,0],False], \
		'星之守护者' : [False,None,[False,1]],'暗星' : [False,0,[False,1],0],'爆破专家' : [False,None,[False,1]],'源计划' : [False,None,[False,1],0],\
		'护卫' : [False,None,[False,1]],'星舰龙神' : [False,None,[False,0]], '虚空' : [False,None,[False,0]], '先锋' : [False,None,[False,0]], \
		'银河魔装机神' : [False,None,[False,0]],'异星人' : [False,None,[False,0]]} 		
# 	标志_行为标志
class Move_flag(object):
	def __init__(self):
		self.normal_attack = False                       	 	# 普攻行为标志
		self.show_normal_attack = [False,0.3,0,Time_count()]   	# 显示普攻图标标志|默认显示0.3s|模式：0 = 普通模式；1 = 暴击且不被闪避;2 = 被闪避
		self.cast_spell = False									# 施法行为标志
		self.show_cast_spell = [False,1,None]					# 显示技能图标标志，默认显示1s，技能名
		self.stop = False										# 无行为行为标志
# 	标志_状态标志
class Condition_flag(object):
	def __init__(self):
		self.buff_shield_flag = False							# 护盾状态标志
		self.debuff_dizz_flag = False							# 眩晕状态标志
		self.debuff_frozen_flag = False 						# 冰冻状态标志
		self.buff_matigation_flag = False						# 减伤状态标志
		self.debuff_injury_flag = False                     	# 重伤状态标志
		self.debuff_silence_flag = False 						# 沉默状态标志
		self.debuff_disarm_flag = False 						# 缴械状态标志
		self.buff_invincible_flag = False 						# 无敌状态标志
		self.buff_unstoppable_flag = False 						# 不可阻挡状态标志
		self.buff_magic_shield_flag = False 					# 魔法护盾状态标志		
		self.death_flag = False       							# 死亡状态标志
		self.miss_flag = [False,False] 							# 不可选取状态标志|状态结束标志
		self.buff_fervor_flag = False 							# 炽热状态标志
		self.buff_iron_flag = [False,True] 						# 钢铁状态标志|状态未触发标志
		self.debuff_burn_flag = False 							# 灼烧状态标志
		self.debuff_poisoning_flag = [False,0]         			# 中毒状态标志|剧毒羁绊(0=2羁绊，1=3羁绊)
		self.debuff_electrification_flag = False      			# 感电状态标志
		self.suppress = [False,False]							# 被压制标志|施法者标志
		self.debuff_taunt_flag = False 							# 嘲讽状态标志
		self.debuff_broken_flag = False 						# 破法状态标志
# 	标志_特殊标志
class Special_flag(object):
	def __init__(self):
		self.force_spell = False 								# 强制施法标志
		self.get_weapon_flag = [False,False]					# 获得武器标志
		self.kill = [False,None,None,None,0] 					# 造成击杀标志
		self.death_deal = False 								# 死亡处理标志
		self.extra_heal_flag = False   							# 过量治疗标志
		# 受到效果显示
		self.effect = {'祈愿' : [False,0.7], '冲击之潮' : [False,0.7], '烈焰风暴' : [False,0.7], '曲光屏障' : [False,0.7], \
		'光之祭献' : [False,0.7], '卢登回声' : [False,0.7], '狂热电刀' : [False,0.7], '离子火花' : [False,0.7], '冰脉护手' : [False,0.7], \
		'魂引之灯' : [False,1], '羊灵生息' : [False,0.7], '沙兵攻击' : [False,0.5], '安魂曲' : [False,0.7], '魔偶攻击' : [False,0.5], \
		'冰风暴' : [False,0], '月光' : [False,0.7], '净化剑刃' : [False,0.7], '活体大炮' : [False,1], '来自艾卡西亚的惊喜' : [False,1], \
		'落雷' : [False,0.7], '荧焰' : [False,0.5], '飞轮' : [False,0.7], '月之驻灵' : [False,0.5], '天雷' : [False,0.5], '提伯斯攻击' : [False,0.7], \
		'欺诈宝珠' : [False,0.5], '金色卡牌' : [False,0.7], '红色卡牌' : [False,0.7], '蓝色卡牌' : [False,0.7], '时间' : [False,0.7], \
		'皮克斯攻击' : [False,0.5], '鼓舞' : [False,0], '陨星' : [False,0.7], '轰炸' : [False,0.5], '鱼骨头' : [False,0.5], '圆盾' : [False,0.7], \
		'炮台攻击' : [False,0.5], '古灵精怪' : [False,0.7], '死亡祭献' : [False,0.7], '闪电链' : [False,0.7]}
		# 受到光环显示
		self.halo = {'冰霜之心' : False, '基克先驱' : False, '深渊面具' : False}
		# 死者领域标志
		self.dead_area = [False,None]
		# 赐福之土标志
		self.bless_land = [False,0.1]
		# 千珏之印标志
		self.Kindred_sign = False
		# 雷缚印标志
		self.thunder_sign = 0
		# 血红之池标志
		self.blood_pool = [False,False]
		# 护体毒雾标志
		self.toxic_smog = False
		# 天雷标志
		self.thunderbolt = False
		# 清辉标记
		self.qh_sign = False
		# 夜凝标记
		self.yn_sign = False
		# 不受减攻速影响标志：Not affected by attack speed reduction effect
		self.Nabasre_flag = False
		# 忍者的能量（查克拉）机制标志
		self.chakra_flag = False
		# 赛博屏障标志
		self.parclose_flag = False
		# 日光标志
		self.sunlight_sign = [False,50]
		# 龙血标记
		self.dragon_sign = False
		# 时间静止标志
		self.motionless_flag = False
		# 孤立无援标记(out on a limb)
		self.ooal_sign = False
		# 波比屏障
		self.obstacle_flag = [False,None]
		# 古灵精怪标志
		self.odd = [False,False]
		# 挑战状态标志
		self.challenge = [False,None,False]
#	标志_伤害计算标志
class Damage_calculation_flag(object):
	def __init__(self):
		self.normal_attack = False 								# 普攻伤害计算标志
		self.spell_attack = False      							# 技能伤害计算标志
		self.total_attack =  False								# 总伤害计算标志
	# 判断是否造成伤害
	def Total_damage_judg(self):
		self.total_attack = self.normal_attack or self.spell_attack
#	标志_武器标志
class Weapon_flag(object):
	def __init__(self):
		self.lzzr = [False,0,False,[10,15]]
		self.jrss = [False,0.02]
		self.sjzm = [False,False,0.12]
		# 基克先驱
		self.jkxq = [False,0.15,[False,False,False],0.2]
		self.shts = [False,False,False,400,2]
		self.yxjj = [False,0.55,10]
		# 科技枪刃
		self.kjqr = [False,0.35,0.4]
		# 无尽之刃
		self.wjzr = [False,[0.1,1],False,[0.15,1.1]]
		self.jshp = [False,[0.1,0.1]]
		self.krdd = [False,0,50,False,0]
		self.blsf = [False,[2.0,1.5],0]
		self.hyzw = [False,False,0]
		self.fljf = [False,False,False,'额外目标：无',0.35]
		self.gszn = [False,0.04,0]
		self.fxtx = [False,[45,3]]
		# 天使之拥
		self.tszy = [False,False,30,40]
		# 神圣救赎
		self.ssjs = [False,True,300,0.3,[False,Time_count(),2.5],[333,1.5]]
		# 冰霜之心
		self.bszx = [False,0.15,[False,False,False],0.2]
		self.cmbs = [False,[0.33,2.5],0]
		# 卢登回声
		self.ldhs = [False,False,False,90,None,110]
		self.zyzs = [False,0,[0.3,30],[0,0]]
		self.ktkj = [False,0,0.025,40]
		self.ttjj = [False,[0,25],[1,0.02,180,180],False]
		# 深渊面具
		self.symj = [False,False,1,0.25,[False,False,False],0.3]
		self.swmd = [False,[8,35],False]
		self.fjzz = [False,True,4]
		# 荆棘之甲
		self.jjzj = [False,[0.85,3],1]
		self.zjmd = [False,[0.30,2.5],0]
		# 烈阳之匣
		self.lyzx = [False,[250,6],[280,8]]
		self.bmhs = [False,[0.1,0.05],False,0]
		# 巨龙之牙
		self.jlzy = [False,0.5,0.65]
		self.lzhh = [False,False,90,0]
		self.sypf = [False,30,False]
		# 灭世之帽
		self.mszm = [False,0.5,0.7]
		self.zgqt = [False,1,False,0,0.05]
		self.qzst = False
		self.yxmr = [False,20,False,30]
		self.sbzg = [False,0.4,False,0,0.08]
		self.wsfm = [False,20,[False,10,2.5],False]
		self.jdzc = [False,1,False,0]
		self.jsbj = [False,0,[6,5,0.02,0.02],0,False]
		self.crxl = [False,False,[0.25,0.25,5],False]
		self.bbrz = [False,[Time_count(),1],5]
		self.haqg = [False,0.08,[0,6]]
		self.fshf = [False,0.04,False,0]
		self.qfzl = [False,0.15,False,0]
		self.ltjl = [False,30,2,False,0]
		self.rgkx = [False,50,0.20,False,0]
		self.pbwz = [False,0.03]
		self.yslj = [False,20,0.35,False,0]
		self.ayhx = [False,[False,Time_count(),6],0.65,0]
		self.bpzd = [False,50,False,0]
		self.clxz = [False,0.10,4,False,False,[Time_count(),5]]
		self.mhgz = [False,15,False,0]
		self.yzfr = [False,15,False,[Time_count(),12],0]
		self.xsfq = [False,0.15]
		self.hazx = [False,150,5,False,0]
		self.syxj = [False,0.4,0.4,False]
		self.xkzm = [False]
		self.jzfy = [False,False]
		self.jxjts = [False,0.7,False]

# 状态
class Condition(object):
	def __init__(self):
		self.shield = Shield()									# 护盾状态
		self.dizz = Dizz()										# 眩晕状态
		self.frozen = Frozen() 									# 冰冻状态
		self.matigation = Matigation()							# 减伤状态
		self.injury = Injury()                                  # 重伤状态
		self.silence = Silence()								# 沉默状态
		self.disarm = Disarm()									# 缴械状态
		self.invincible = Invincible()							# 无敌状态
		self.unstoppable = Unstoppable() 						# 不可阻挡状态
		self.magic_shield = Magic_shield()						# 魔法护盾状态
		self.miss = Miss() 										# 不可选取状态
		self.fervor = Fervor() 									# 炽热状态
		self.iron = Iron() 										# 钢铁状态
		self.burn = Burn() 										# 灼烧状态
		self.poisoning = Poisoning() 							# 中毒状态
		self.electrification = Electrification() 				# 感电状态
		self.suppress = Suppress() 								# 压制状态
		self.taunt = Taunt() 									# 嘲讽状态
		self.broken = Broken() 									# 破法状态
	# 状态处理
	def Condition_deal(self,flag,champion):
		# 护盾状态
		if flag.condition_flag.buff_shield_flag:
			self.shield.Shield_condition_deal(flag)
		# 眩晕状态
		if flag.condition_flag.debuff_dizz_flag:
			self.dizz.Dizz_condition_deal(flag,champion)
		# 冰冻状态
		if flag.condition_flag.debuff_frozen_flag:
			self.frozen.Frozen_condition_deal(flag,champion)
		# 减伤状态
		if flag.condition_flag.buff_matigation_flag:
			self.matigation.Matigation_condition_deal(flag,champion)
		# 重伤状态
		if flag.condition_flag.debuff_injury_flag:
			self.injury.Injury_condition_deal(flag)
		# 沉默状态
		if flag.condition_flag.debuff_silence_flag:
			self.silence.Silence_condition_deal(flag)
		# 缴械状态
		if flag.condition_flag.debuff_disarm_flag:
			self.disarm.Disarm_condition_deal(flag,champion)
		# 无敌状态
		if flag.condition_flag.buff_invincible_flag:
			self.invincible.Invincible_condition_deal(flag,champion)
		# 不可阻挡状态
		if flag.condition_flag.buff_unstoppable_flag:
			self.unstoppable.Unstoppable_condition_deal(flag)
		# 魔法护盾状态
		if flag.condition_flag.buff_magic_shield_flag:
			self.magic_shield.Magic_shield_condition_deal(flag,champion)
		# 不可选取状态
		if flag.condition_flag.miss_flag[0]:
			self.miss.Miss_condition_deal(flag,champion)
		# 炽热状态
		if flag.condition_flag.buff_fervor_flag:
			self.fervor.Fervor_condition_deal(flag,champion)
		# 钢铁状态
		if flag.condition_flag.buff_iron_flag[0]:
			self.iron.Iron_condition_deal(flag)
		# 灼烧状态
		if flag.condition_flag.debuff_burn_flag:
			self.burn.Burn_condition_deal(flag,champion)
		# 中毒状态
		if flag.condition_flag.debuff_poisoning_flag[0]:
			self.poisoning.Poisoning_condition_deal(flag)
		# 感电状态
		if flag.condition_flag.debuff_electrification_flag:
			self.electrification.Electrification_condition_deal(flag)
		# 压制状态
		if flag.condition_flag.suppress[0]:
			self.suppress.Suppress_condition_deal(champion)
		# 嘲讽状态
		if flag.condition_flag.debuff_taunt_flag:
			self.taunt.Taunt_condition_deal(champion)
	# 清除状态
	def Clean_condition(self,champion,mode):  # mode = 0 全清除，mode = 1 复活甲效果，清除除重伤意外的状态，其他： 只清除debuff（无敌状态不考虑在内）
		self.dizz.Clean(champion.flag,champion)
		self.frozen.Clean(champion.flag,champion)
		self.silence.Clean(champion.flag)
		if not champion.champion.name == 'AurelionSol':
			self.disarm.Clean(champion.flag,champion)
		self.burn.Clean(champion.flag)
		self.poisoning.Clean(champion.flag)
		self.electrification.Clean(champion.flag)
		self.taunt.Clean(champion)
		if champion.flag.condition_flag.debuff_broken_flag:
			self.broken.Clean(champion)
		# 移除清辉标记、夜凝标记、日光标记、龙血标记
		champion.flag.special_flag.qh_sign = False
		champion.flag.special_flag.yn_sign = False
		champion.flag.special_flag.sunlight_sign[0] = False
		champion.flag.special_flag.dragon_sign = False
		if mode != 1:
			self.injury.Clean(champion.flag)
		if mode == 0 or mode == 1:
			self.shield.Clean(champion.flag)
			self.matigation.Clean(champion.flag,champion)
			self.unstoppable.Clean(champion.flag)
			self.magic_shield.Clean(champion.flag)
			if champion.flag.weapon_flag.crxl[1]:
				self.fervor.Clean(champion.flag,champion)
# 	状态_护盾状态
class Shield(object):
	def __init__(self):
		self.value = 0											# 护盾值
		self.time = 0											# 护盾持续时间
		self.time_count = Time_count()							# 护盾持续时间计数值
	# 护盾期间判断
	def Shield_period(self):
		time_count_flag = self.time_count.Duration(self.time)
		if (int(self.value) > 0) and (not time_count_flag):
			return False # 继续处于护盾期间
		else:
			return True
	# 护盾状态清除
	def Clean(self, flag):
		# 护盾值清零
		self.value = 0
		# 护盾持续时间计数值清零
		self.time_count.value = 0
		# 状态标志处理
		flag.condition_flag.buff_shield_flag = False
	# 护盾状态处理
	def Shield_condition_deal(self, flag):
		shield_period_end_flag = self.Shield_period()
		if shield_period_end_flag:
			self.Clean(flag)
	# 加盾
	def Add_shield(self,champion,add_shield_value,add_shield_time):
		champion.condition.shield.value += add_shield_value
		champion.condition.shield.time = Max(add_shield_time,int((champion.condition.shield.time*100 - champion.condition.shield.time_count.value)/100))
		champion.condition.shield.time_count.value = 0
		champion.flag.condition_flag.buff_shield_flag = True		
#	状态_眩晕状态
class Dizz(object):
	def __init__(self):
		self.time = 0											# 眩晕持续时间
		self.time_count = Time_count()							# 眩晕持续时间计数值
	# 眩晕状态清除
	def Clean(self, flag, champion):
		self.time_count.value = 0
		# 状态标志处理
		flag.condition_flag.debuff_dizz_flag = False
		champion.move.current_move = 'normal_attack'
		# 重置普攻
		champion.champion.attack_attribute.normal_attack_time_count = 0
	# 眩晕状态处理
	def Dizz_condition_deal(self, flag, champion):
		# 眩晕期间判断
		dizz_period_end_flag = self.time_count.Duration(self.time)
		if dizz_period_end_flag:
			self.Clean(flag,champion)
		else:
			champion.move.current_move = 'stop'
	# 加眩晕状态
	def Add_dizz(self,champion,add_dizz_time):
		champion.condition.dizz.time = Max(add_dizz_time,int((champion.condition.dizz.time*100 - champion.condition.dizz.time_count.value)/100))
		champion.condition.dizz.time_count.value = 0
		champion.flag.condition_flag.debuff_dizz_flag = True
#	状态_冰冻状态
class Frozen(object):
	def __init__(self):
		self.time = 0											# 冰冻持续时间
		self.time_count = Time_count()							# 冰冻持续时间计数值
	# 冰冻状态清除
	def Clean(self, flag, champion):
		self.time_count.value = 0
		# 状态标志处理
		flag.condition_flag.debuff_frozen_flag = False
		champion.move.current_move = 'normal_attack'
		# 重置普攻
		champion.champion.attack_attribute.normal_attack_time_count = 0
	# 冰冻状态处理
	def Frozen_condition_deal(self, flag, champion):
		# 冰冻期间判断
		frozen_period_end_flag = self.time_count.Duration(self.time)
		if frozen_period_end_flag:
			self.Clean(flag,champion)
		else:
			champion.move.current_move = 'stop'
	# 加冰冻状态
	def Add_frozen(self,champion,add_frozen_time):
		champion.condition.frozen.time = Max(add_frozen_time,int((champion.condition.frozen.time*100 - champion.condition.frozen.time_count.value)/100))
		champion.condition.frozen.time_count.value = 0
		champion.flag.condition_flag.debuff_frozen_flag = True
#	状态_减伤状态
class Matigation(object):
	def __init__(self):
		self.value = 1											# 减伤倍数
		self.time = 0											# 减伤持续时间
		self.time_count = Time_count()							# 减伤持续时间计数值
	# 减伤状态清除
	def Clean(self, flag, champion):
		self.time_count.value = 0
		# 减伤倍数重置
		self.value = 1
		# 状态标志处理 
		flag.condition_flag.buff_matigation_flag = False
	# 减伤状态处理
	def Matigation_condition_deal(self, flag, champion):
		# 减伤期间判断
		matigation_period_end_flag = self.time_count.Duration(self.time)
		if matigation_period_end_flag:
			self.Clean(flag,champion)
	# 加减伤状态
	def Add_matigation(self,champion,matigation_value,add_matigation_time):
		champion.condition.matigation.value = matigation_value
		champion.condition.matigation.time = Max(add_matigation_time,int((champion.condition.matigation.time*100 - champion.condition.matigation.time_count.value)/100))
		champion.condition.matigation.time_count.value = 0
		champion.flag.condition_flag.buff_matigation_flag = True
# 	状态_重伤状态
class Injury(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 重伤状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		# 状态标志处理 
		flag.condition_flag.debuff_injury_flag = False
	# 重伤状态处理
	def Injury_condition_deal(self, flag):
		# 重伤期间判断
		injury_period_end_flag = self.time_count.Duration(self.time)
		if injury_period_end_flag:
			self.Clean(flag)
	# 加重伤状态
	def Add_injury(self,champion,add_injury_time):
		champion.condition.injury.time = Max(add_injury_time,int((champion.condition.injury.time*100 - champion.condition.injury.time_count.value)/100))
		champion.condition.injury.time_count.value = 0
		champion.flag.condition_flag.debuff_injury_flag = True
# 	状态_沉默状态
class Silence(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 沉默状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		# 状态标志处理 
		flag.condition_flag.debuff_silence_flag = False
	# 沉默状态处理
	def Silence_condition_deal(self, flag):
		# 沉默期间判断
		silence_period_end_flag = self.time_count.Duration(self.time)
		if silence_period_end_flag:
			self.Clean(flag)
	# 计算沉默时间
	def Add_silence(self,champion,add_silence_time):
		champion.condition.silence.time = Max(add_silence_time,int((champion.condition.silence.time*100 - champion.condition.silence.time_count.value)/100))
		champion.condition.silence.time_count.value = 0
		champion.flag.condition_flag.debuff_silence_flag = True
# 	状态_缴械状态
class Disarm(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 缴械状态清除
	def Clean(self, flag, champion):
		self.time_count.value = 0
		# 状态标志处理 
		flag.condition_flag.debuff_disarm_flag = False
		# 重置普攻
		champion.champion.attack_attribute.normal_attack_time_count = 0
	# 缴械状态处理
	def Disarm_condition_deal(self, flag, champion):
		# 缴械期间判断
		disarm_period_end_flag = self.time_count.Duration(self.time)
		if disarm_period_end_flag:
			self.Clean(flag, champion)
	# 计算缴械时间
	def Add_disarm(self,champion,add_disarm_time):
		champion.condition.disarm.time = Max(add_disarm_time,int((champion.condition.disarm.time*100 - champion.condition.disarm.time_count.value)/100))
		champion.condition.disarm.time_count.value = 0
		champion.flag.condition_flag.debuff_disarm_flag = True
#	状态_无敌状态
class Invincible(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 无敌状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		# 状态标志处理 
		flag.condition_flag.buff_invincible_flag = False
	# 无敌状态处理
	def Invincible_condition_deal(self, flag, champion):
		# 无敌期间判断
		invincible_period_end_flag = self.time_count.Duration(self.time)
		if invincible_period_end_flag:
			self.Clean(flag)
	# 计算无敌时间
	def Add_invincible(self,champion,add_invincible_time):
		champion.condition.invincible.time = Max(add_invincible_time,int((champion.condition.invincible.time*100 - champion.condition.invincible.time_count.value)/100))
		champion.condition.invincible.time_count.value = 0
		champion.flag.condition_flag.buff_invincible_flag = True
#	状态_不可阻挡状态
class Unstoppable(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 不可阻挡状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		# 状态标志处理 
		flag.condition_flag.buff_unstoppable_flag = False
	# 不可阻挡状态处理
	def Unstoppable_condition_deal(self, flag):
		# 不可阻挡期间判断
		unstoppable_period_end_flag = self.time_count.Duration(self.time)
		if unstoppable_period_end_flag:
			self.Clean(flag)
	# 计算不可阻挡时间
	def Add_unstoppable(self,champion,add_unstoppable_time):
		champion.condition.unstoppable.time = Max(add_unstoppable_time,int((champion.condition.unstoppable.time*100 - champion.condition.unstoppable.time_count.value)/100))
		champion.condition.unstoppable.time_count.value = 0
		champion.flag.condition_flag.buff_unstoppable_flag = True
#	状态_魔法护盾状态
class Magic_shield(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 魔法护盾状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		# 状态标志处理
		flag.condition_flag.buff_magic_shield_flag = False
		# 夜之锋刃处理
		flag.weapon_flag.yzfr[2] = False
		flag.weapon_flag.yzfr[4] += 1
	# 魔法护盾状态处理
	def Magic_shield_condition_deal(self, flag, champion):
		# 魔法护盾期间判断
		magic_shield_period_end_flag = self.time_count.Duration(self.time)
		if magic_shield_period_end_flag:
			self.Clean(flag)
	# 计算魔法护盾时间
	def Add_magic_shield(self,champion,add_magic_shield_time):
		champion.condition.magic_shield.time = Max(add_magic_shield_time,int((champion.condition.magic_shield.time*100 - champion.condition.magic_shield.time_count.value)/100))
		champion.condition.magic_shield.time_count.value = 0
		champion.flag.condition_flag.buff_magic_shield_flag = True
#	状态_不可选取状态
class Miss(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 不可选取状态处理
	def Miss_condition_deal(self, flag, champion):
		flag.condition_flag.miss_flag[1] = False
		# 不可选取期间判断
		miss_period_end_flag = self.time_count.Duration(self.time)
		if miss_period_end_flag:
			# 重置普攻
			champion.champion.attack_attribute.normal_attack_time_count = 0
			# 状态标志处理
			flag.condition_flag.miss_flag[0] = False
			flag.condition_flag.miss_flag[1] = True
			# 处理巫师法帽效果
			if flag.weapon_flag.wsfm[3]:
				flag.weapon_flag.wsfm[3] = False
			# 处理守护天使效果
			elif flag.weapon_flag.shts[2]:
				# 恢复生命值
				champion.champion.hp.HP_restore(flag.weapon_flag.shts[3],champion.champion,champion)
				flag.weapon_flag.shts[2] = False
			# 处理弗拉基米尔的血红之池
			elif flag.special_flag.blood_pool[0]:
				flag.special_flag.blood_pool[0] = False
			# 处理菲兹的古灵精怪
			elif flag.special_flag.odd[0]:
				flag.special_flag.odd[0] = False
				champion.Odd(1)
				# 清除除重伤意外的状态
				champion.condition.Clean_condition(champion,1)

	# 计算不可选取时间
	def Add_miss(self,champion,add_miss_time):
		champion.condition.miss.time = Max(add_miss_time,int((champion.condition.miss.time*100 - champion.condition.miss.time_count.value)/100))
		champion.condition.miss.time_count.value = 0
		champion.flag.condition_flag.miss_flag[0] = True
		champion.flag.condition_flag.miss_flag[1] = False
		# 重置普攻
		champion.champion.attack_attribute.normal_attack_time_count = 0
		if champion.champion.name == 'Yi':
			champion.champion.attack_attribute.attack_count = 0
		champion.flag.condition_flag.suppress[0] = False
# 	状态_炽热状态
class Fervor(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 炽热状态清除
	def Clean(self, flag, champion):
		self.time_count.value = 0
		# 恢复攻速、生命偷取
		if champion.champion.name == 'Jhin':
			champion.As2cr(1 / (1 + flag.weapon_flag.crxl[2][0]))
		else:
			champion.champion.attack_attribute.attack_speed /= (1 + flag.weapon_flag.crxl[2][0])
		champion.champion.hemophagia -= flag.weapon_flag.crxl[2][1]
		flag.weapon_flag.crxl[1] = False
		# 状态标志处理 
		flag.condition_flag.buff_fervor_flag = False
	# 炽热状态处理
	def Fervor_condition_deal(self, flag, champion):
		# 炽热期间判断
		fervor_period_end_flag = self.time_count.Duration(self.time)
		if fervor_period_end_flag:
			self.Clean(flag,champion)
		else: # 提升攻速、获得生命偷取
			if not flag.weapon_flag.crxl[1]:
				if champion.champion.name == 'Jhin':
					champion.As2cr(1 + flag.weapon_flag.crxl[2][0])
				else:
					champion.champion.attack_attribute.attack_speed *= (1 + flag.weapon_flag.crxl[2][0])
				champion.champion.hemophagia += flag.weapon_flag.crxl[2][1]
				champion.flag.weapon_flag.crxl[1] = True

	# 加炽热状态
	def Add_fervor(self,champion,add_fervor_time):
		champion.condition.fervor.time = Max(add_fervor_time,int((champion.condition.fervor.time*100 - champion.condition.fervor.time_count.value)/100))
		champion.condition.fervor.time_count.value = 0
		champion.flag.condition_flag.buff_fervor_flag = True
#	状态_钢铁状态
class Iron(object):
	def __init__(self):
		self.value = 1
		self.time = 0											# 钢铁持续时间
		self.time_count = Time_count()							# 钢铁持续时间计数值
	# 钢铁状态清除
	def Clean(self, flag):
		self.value = 1
		self.time_count.value = 0
		# 状态标志处理 
		flag.condition_flag.buff_iron_flag[0] = False
	# 钢铁状态处理
	def Iron_condition_deal(self, flag):
		# 钢铁期间判断
		iron_period_end_flag = self.time_count.Duration(self.time)
		if iron_period_end_flag:
			self.Clean(flag)
	# 加钢铁状态
	def Add_iron(self,champion,add_iron_time):
		self.value = 0
		self.time = add_iron_time
		self.time_count.value = 0
		champion.flag.condition_flag.buff_iron_flag = [True,False]
#	状态_灼烧状态
class Burn(object):
	def __init__(self):
		self.time = 0											# 灼烧持续时间
		self.time_count = Time_count()							# 灼烧持续时间计数值
		self.dot_time = 0.99									# 灼烧伤害间隔时间
		self.dot_time_count = Time_count()						# 灼烧伤害计时
		self.source = None 										# 灼烧伤害来源
	# 灼烧状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		self.dot_time_count.value = 0
		# 状态标志处理
		flag.condition_flag.debuff_burn_flag = False
	# 灼烧状态处理
	def Burn_condition_deal(self, flag, champion):
		# 灼烧期间判断
		burn_period_end_flag = self.time_count.Duration(self.time)
		if burn_period_end_flag:
			self.Clean(flag)
		else:
			dot_end_flag = self.dot_time_count.Duration(self.dot_time)
			if dot_end_flag and not champion.flag.condition_flag.miss_flag[0] and not champion.flag.condition_flag.buff_invincible_flag\
			and not champion.flag.condition_flag.buff_iron_flag[0]:
				if version[0] == 3:
					dot_damage = champion.champion.hp.max_value * rela_dic['地狱火'][1][5] * self.source.champion.attack_attribute.spell_power
				else:
					dot_damage = champion.champion.hp.max_value * self.source.flag.rela_flag['地狱火'][1] * self.source.champion.attack_attribute.spell_power
				champion.champion.hp.HP_reduce(dot_damage,self.source,champion)
				# 触发科技枪刃效果
				if self.source.flag.weapon_flag.kjqr[0]: 								
					hp_restore_value = self.source.flag.weapon_flag.kjqr[1] * dot_damage
					self.source.champion.hp.HP_restore(hp_restore_value,self.source.champion,self.source)
				# 累计造成伤害
				self.source.champion.attack_attribute.all_damage.real_damage += dot_damage
				self.source.champion.attack_attribute.all_damage.Total_damage_calculation()
	# 加灼烧状态
	def Add_burn(self,champion,add_burn_time):
		champion.condition.burn.time = Max(add_burn_time,int((champion.condition.burn.time*100 - champion.condition.burn.time_count.value)/100))
		champion.condition.burn.time_count.value = 0
		champion.flag.condition_flag.debuff_burn_flag = True
#	状态_中毒状态
class Poisoning(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
	# 中毒状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		# 状态标志处理 
		flag.condition_flag.debuff_poisoning_flag[0] = False
	# 中毒状态处理
	def Poisoning_condition_deal(self, flag):
		# 中毒期间判断
		poisoning_period_end_flag = self.time_count.Duration(self.time)
		if poisoning_period_end_flag:
			self.Clean(flag)
	# 计算中毒时间
	def Add_poisoning(self,champion,add_poisoning_time,mode):
		champion.condition.poisoning.time = Max(add_poisoning_time,int((champion.condition.poisoning.time*100 - champion.condition.poisoning.time_count.value)/100))
		champion.condition.poisoning.time_count.value = 0
		champion.flag.condition_flag.debuff_poisoning_flag = [True,mode]
#	状态_感电状态
class Electrification(object):
	def __init__(self):
		self.time = 0
		self.time_count = Time_count()
		# 感电状态伤害增幅
		self.amplification = 1.5
	# 感电状态清除
	def Clean(self, flag):
		self.time_count.value = 0
		# 状态标志处理
		flag.condition_flag.debuff_electrification_flag = False
	# 感电状态处理
	def Electrification_condition_deal(self, flag):
		# 感电期间判断
		electrification_period_end_flag = self.time_count.Duration(self.time)
		if electrification_period_end_flag:
			self.Clean(flag)
	# 加感电状态
	def Add_electrification(self,champion,add_electrification_time):
		champion.condition.electrification.time = Max(add_electrification_time,int((champion.condition.electrification.time*100 - champion.condition.electrification.time_count.value)/100))
		champion.condition.electrification.time_count.value = 0
		champion.flag.condition_flag.debuff_electrification_flag = True
#	状态_压制状态
class Suppress(object):
	def __init__(self):
		pass
	# 压制状态清除
	def Clean(self,champion):
		# 状态标志处理
		champion.flag.condition_flag.suppress[0] = False
		champion.move.current_move = 'normal_attack'
		# 重置普攻
		champion.champion.attack_attribute.normal_attack_time_count = 0
	# 压制状态处理
	def Suppress_condition_deal(self,champion):
		champion.move.current_move = 'stop'
	# 加压制状态
	def Add_suppress(self,champion):
		champion.flag.condition_flag.suppress[0] = True
		champion.move.current_move = 'stop'
#	状态_嘲讽状态
class Taunt(object):
	def __init__(self):
		self.target = [None,None]   	# 原先目标|嘲讽后目标
		self.time = 0
		self.time_count = Time_count()
	# 嘲讽状态清除
	def Clean(self,champion):
		# 状态标志处理
		champion.flag.condition_flag.debuff_taunt_flag = False
		# 目标恢复
		if self.target[0] != None:
			if not self.target[0].flag.condition_flag.death_flag and not self.target[0].flag.condition_flag.miss_flag[0]:
				champion.enemy = self.target[0]
		self.__init__()
		# 重置普攻
		champion.champion.attack_attribute.normal_attack_time_count = 0
	# 嘲讽状态处理
	def Taunt_condition_deal(self,champion):
		# 嘲讽期间判断
		if self.time_count.Duration(self.time) or self.target[1].flag.condition_flag.death_flag or self.target[1].flag.condition_flag.miss_flag[0]:
			self.Clean(champion)
	# 加嘲讽状态
	def Add_taunt(self,champion,add_taunt_time,caster):
		champion.flag.condition_flag.debuff_taunt_flag = True
		champion.condition.taunt.target = [champion.enemy,caster]
		champion.enemy = caster
		champion.condition.taunt.time = Max(add_taunt_time,int((champion.condition.taunt.time*100 - champion.condition.taunt.time_count.value)/100))
		champion.condition.taunt.time_count.value = 0
#	状态_破法状态
class Broken(object):
	def __init__(self):
		self.value = 0.4
	# 破法状态清除
	def Clean(self, champion):
		# 恢复最大法力值
		champion.champion.mp.max_value /= (1 + self.value)
		# 状态标志处理 
		champion.flag.condition_flag.debuff_broken_flag = False
	# 处理破法效果
	def Add_brokrn(self,champion):
		if not champion.flag.condition_flag.debuff_broken_flag and champion.champion.mp.max_value > 0:
			champion.flag.condition_flag.debuff_broken_flag = True
			champion.champion.mp.max_value *= (1 + self.value)

# 行为
class Move(object):
	def __init__(self):
		self.current_move = 'normal_attack'                 	# 当前行为
	# 施法判断
	def Cast_spell_judg(self,champion):
		# 奥莉安娜在魔偶移动状态时不能施法
		if not ((champion.champion.name == 'Orianna' and golem.moving_flag) or (champion.champion.name == 'Lulu' and pix.moving_flag)):
			# 判断是否达到最大蓝量
			if (champion.champion.mp.value == champion.champion.mp.max_value or champion.champion.skill.continuous[1]) \
			and self.current_move != 'stop' and not champion.flag.condition_flag.debuff_taunt_flag:
				self.current_move = 'cast_spell'
	# 行为判断
	def Move_judg(self,champion):
		champion.flag.move_flag.normal_attack = False
		if champion.flag.condition_flag.miss_flag[0]:
			self.current_move = 'stop'
		if self.current_move == 'stop':      	# stop行为：不普攻也不施法
			champion.flag.move_flag.normal_attack = False
			champion.flag.move_flag.cast_spell = False
			if champion.enemy.flag.condition_flag.miss_flag[1] and not champion.enemy.flag.condition_flag.death_flag and not champion.flag.condition_flag.miss_flag[0]:
				self.current_move = 'normal_attack'
			if champion.flag.condition_flag.miss_flag[1] and not champion.enemy.flag.condition_flag.death_flag and not champion.enemy.flag.condition_flag.miss_flag[0]:
				self.current_move = 'normal_attack'
			if not champion.flag.condition_flag.miss_flag[0] and not champion.enemy.flag.condition_flag.miss_flag[0] \
			and not champion.enemy.flag.special_flag.dead_area[0] and not champion.enemy.flag.condition_flag.death_flag \
			and not champion.flag.condition_flag.debuff_dizz_flag and not champion.flag.condition_flag.debuff_frozen_flag \
			and not champion.flag.condition_flag.suppress[0] and not champion.champion.skill.comb[0]:
					self.current_move = 'normal_attack'
			if champion.champion.skill.comb[3]: # 组合技能第一段结束，继续施法(第二段技能)
				self.current_move = 'cast_spell'
				champion.champion.skill.comb[3] = False
		# 烬装弹
		if self.current_move == 'load':
			champion.flag.move_flag.normal_attack = False
			champion.flag.move_flag.cast_spell = False
		# 持续施法技能施法中被眩晕、冰冻、沉默、压制、嘲讽打断
		if champion.champion.skill.continuous[1] and (champion.flag.condition_flag.debuff_dizz_flag or champion.flag.condition_flag.debuff_frozen_flag \
			or champion.flag.condition_flag.debuff_silence_flag or champion.flag.condition_flag.suppress[0] or champion.flag.condition_flag.debuff_taunt_flag \
			or champion.flag.condition_flag.miss_flag[0]) and not champion.flag.condition_flag.suppress[1]:
			champion.champion.skill.continuous[1] = False
			champion.champion.skill.continuous[2] = True
			champion.champion.skill.continuous[3] = True
			champion.flag.move_flag.cast_spell = False
			# 重置普攻
			champion.champion.attack_attribute.normal_attack_time_count = 0
			# 奥恩被打断技能的同时结束不可阻挡状态
			if champion.champion.name == 'Ornn':
				champion.condition.unstoppable.Clean(champion.flag)
			# 易被打断技能的同时结束减伤状态且重置连续普攻计数
			if champion.champion.name == 'Yi':
				champion.condition.matigation.Clean(champion.flag, champion)
				champion.champion.attack_attribute.attack_count = 0
			# 泽拉斯被打断技能时若陨星≤2，则回复法力值
			if champion.champion.name == 'Xerath':
				if not champion.champion.skill.para[0][5].flag.condition_flag.death_flag and not champion.champion.skill.para[0][5].flag.condition_flag.miss_flag[0]:
					champion.enemy = champion.champion.skill.para[0][5]
				if champion.champion.skill.para[0][2] <= champion.champion.skill.para[2][0]:
					champion.champion.mp.Calculation(champion,champion.champion.skill.para[2][1])
					print('泽拉斯被打断技能时若陨星≤%d，回复%d法力值' % (champion.champion.skill.para[2][0],champion.champion.skill.para[2][1]))
			self.current_move = 'normal_attack'
			print('%s被打断施法' % champion.champion.name)
		if self.current_move == 'normal_attack' and (not champion.flag.condition_flag.debuff_dizz_flag) and (not champion.flag.condition_flag.debuff_frozen_flag) and (not champion.flag.condition_flag.debuff_disarm_flag):
			champion.flag.move_flag.normal_attack = True
		elif self.current_move == 'cast_spell':
			if ((not champion.flag.condition_flag.debuff_dizz_flag and not champion.flag.condition_flag.debuff_frozen_flag and not champion.flag.condition_flag.suppress[0])\
			 or champion.flag.special_flag.force_spell) and not champion.flag.condition_flag.suppress[0]:
				champion.flag.move_flag.normal_attack = False
				champion.flag.move_flag.cast_spell = True

# 武器
class Weapon(object):
	def __init__(self,pos_num = 0):
		self.weapon = [None, None, None ,None, None, None]  # 第三个是进阶武器,后三个是计算窃贼手套效果时用到的

	# 装备基础武器
	def Equip_weapon(self,weapon_number,champion):
		if self.weapon[weapon_number - 1] == '暴风大剑':
			if champion.flag.rela_flag['源计划'][0]:
				champion.champion.attack_attribute.AD += (10 * champion.flag.rela_flag['源计划'][1])
				champion.flag.rela_flag['源计划'][2][0] = True
			else:
				champion.champion.attack_attribute.AD += 10
			if champion.champion.name == 'Jhin':
				champion.champion.attack_attribute.basic_AD += 10
		elif self.weapon[weapon_number - 1] == '反曲之弓':
			if champion.champion.name == 'Jhin':
				champion.As2cr(1.15)
			else:
				if champion.flag.rela_flag['源计划'][0]:
					champion.champion.attack_attribute.attack_speed *= (math.pow(1.15, champion.flag.rela_flag['源计划'][1]))
					champion.flag.rela_flag['源计划'][2][0] = True
				else:
					champion.champion.attack_attribute.attack_speed *= 1.15
		elif self.weapon[weapon_number - 1] == '女神之泪':
			mp_restore_value = 20
			if not champion.flag.special_flag.chakra_flag:
				if champion.flag.rela_flag['源计划'][0]:
					champion.champion.mp.Calculation(champion,mp_restore_value * champion.flag.rela_flag['源计划'][1])
					champion.flag.rela_flag['源计划'][2][0] = True
				else:
					champion.champion.mp.Calculation(champion,mp_restore_value)
		elif self.weapon[weapon_number - 1] == '巨人腰带':
			if champion.flag.rela_flag['源计划'][0]:
				champion.champion.hp.max_value += (200 * champion.flag.rela_flag['源计划'][1])
				champion.champion.hp.value += (200 * champion.flag.rela_flag['源计划'][1])
				champion.flag.rela_flag['源计划'][2][0] = True
			else:
				champion.champion.hp.max_value += 200
				champion.champion.hp.value += 200
		elif self.weapon[weapon_number - 1] == '钢铁锁甲':
			if champion.flag.rela_flag['源计划'][0]:
				champion.champion.defensive_attribute.armor += (25 * champion.flag.rela_flag['源计划'][1])
				champion.flag.rela_flag['源计划'][2][0] = True
			else:
				champion.champion.defensive_attribute.armor += 25
		elif self.weapon[weapon_number - 1] == '负极斗篷':
			if champion.flag.rela_flag['源计划'][0]:
				champion.champion.defensive_attribute.spell_resistance += (20 * champion.flag.rela_flag['源计划'][1])
				champion.champion.defensive_attribute.Add_tenacity(0.1 * champion.flag.rela_flag['源计划'][1])
				champion.flag.rela_flag['源计划'][2][0] = True
			else:
				champion.champion.defensive_attribute.spell_resistance += 20
				champion.champion.defensive_attribute.Add_tenacity(0.1)
		elif self.weapon[weapon_number - 1] == '无用大棒':
			if champion.champion.name == 'Heimerdinger':
				champion.Add_spell_power(0.2)
			else:
				if champion.flag.rela_flag['源计划'][0]:
					champion.champion.attack_attribute.spell_power += (0.2 * champion.flag.rela_flag['源计划'][1])
					champion.flag.rela_flag['源计划'][2][0] = True
				else:
					champion.champion.attack_attribute.spell_power += 0.2
		elif self.weapon[weapon_number - 1] == '格斗手套':
			if champion.flag.rela_flag['源计划'][0]:
				champion.champion.attack_attribute.crit_mechanism.Add_crit(0.1 * champion.flag.rela_flag['源计划'][1])
				champion.flag.rela_flag['源计划'][2][0] = True
			else:
				champion.champion.attack_attribute.crit_mechanism.Add_crit(0.1)
		elif self.weapon[weapon_number - 1] == '金色魔铲':
			if version[0] == 2:
				champion.champion.defensive_attribute.dodge_mechanism.Add_dodge(0.05)
			elif version[0] in (1,3):
				if champion.flag.rela_flag['源计划'][0]:
					champion.champion.defensive_attribute.dodge_mechanism.Add_dodge(0.1 * champion.flag.rela_flag['源计划'][1])
					champion.flag.rela_flag['源计划'][2][0] = True
				else:
					champion.champion.defensive_attribute.dodge_mechanism.Add_dodge(0.1)
		# 武器进阶
		if weapon_number == 2:
			self.Advance_weapon(champion)
	# 奥恩升级武器
	def Super_weapon(self,champion,weapon):
		sw_flag = False
		for i in range(3):
			if champion.friend[i].champion.name == 'Ornn' and not champion.friend[i].flag.condition_flag.death_flag:
				sw_flag = True
				champion.friend[i].champion.skill.extra[2][0][2] = True
				break
		# 源计划羁绊
		if champion.flag.rela_flag['源计划'][0]:
			sw_flag = True
		if sw_flag:
			if weapon == '基克先驱':
				champion.weapon.weapon[2] = '基克聚合'
				champion.flag.weapon_flag.jkxq[1] = champion.flag.weapon_flag.jkxq[3]
			elif weapon == '科技枪刃':
				champion.weapon.weapon[2] = '附魔枪刃'
				champion.flag.weapon_flag.kjqr[1] = champion.flag.weapon_flag.kjqr[2]
			elif weapon == '无尽之刃':
				champion.weapon.weapon[2] = '熔火之刃'
				champion.flag.weapon_flag.wjzr[1] = champion.flag.weapon_flag.wjzr[3]
			elif weapon == '天使之拥':
				champion.weapon.weapon[2] = '天使之吻'
				champion.flag.weapon_flag.tszy[2] = champion.flag.weapon_flag.tszy[3]
			elif weapon == '神圣救赎':
				champion.weapon.weapon[2] = '神圣拯救'
				champion.flag.weapon_flag.ssjs[2] = champion.flag.weapon_flag.ssjs[5][0]
				champion.flag.weapon_flag.ssjs[4][2] = champion.flag.weapon_flag.ssjs[5][1]
			elif weapon == '冰霜之心':
				champion.weapon.weapon[2] = '冰封之心'
				champion.flag.weapon_flag.bszx[1] = champion.flag.weapon_flag.bszx[3]
			elif weapon == '卢登回声':
				champion.weapon.weapon[2] = '卢登脉冲'
				champion.flag.weapon_flag.ldhs[3] = champion.flag.weapon_flag.ldhs[5]
			elif weapon == '深渊面具':
				champion.weapon.weapon[2] = '炼狱面具'
				champion.flag.weapon_flag.symj[3] = champion.flag.weapon_flag.symj[5]
			elif weapon == '荆棘之甲':
				champion.weapon.weapon[2] = '荆棘之咬'
				champion.flag.weapon_flag.jjzj[1][0] = champion.flag.weapon_flag.jjzj[2]
			elif weapon == '烈阳之匣':
				champion.weapon.weapon[2] = '烈阳之环'
				champion.flag.weapon_flag.lyzx[1] = champion.flag.weapon_flag.lyzx[2]
			elif weapon == '巨龙之牙':
				champion.weapon.weapon[2] = '邪龙之牙'
				champion.flag.weapon_flag.jlzy[1] = champion.flag.weapon_flag.jlzy[2]
			elif weapon == '灭世之帽':
				champion.weapon.weapon[2] = '灭世之冠'
				champion.flag.weapon_flag.mszm[1] = champion.flag.weapon_flag.mszm[2]
	# 合成进阶武器
	def Advance_weapon(self,champion):
		if self.weapon[0] + self.weapon[1] == '暴风大剑暴风大剑':
			self.weapon[2] = '领主之刃'
			champion.flag.weapon_flag.lzzr[0] = True
			# 领主之刃效果1，获得额外15点物攻
			champion.champion.attack_attribute.AD += champion.flag.weapon_flag.lzzr[3][0]
		elif self.weapon[0] + self.weapon[1] in ('暴风大剑反曲之弓','反曲之弓暴风大剑'):
			self.weapon[2] = '巨人杀手'
			champion.flag.weapon_flag.jrss[0] = True
		elif self.weapon[0] + self.weapon[1] in ('暴风大剑女神之泪','女神之泪暴风大剑'):
			self.weapon[2] = '朔极之矛'
			champion.flag.weapon_flag.sjzm[0] = True
		elif self.weapon[0] + self.weapon[1] in ('暴风大剑巨人腰带','巨人腰带暴风大剑'):
			self.weapon[2] = '基克先驱'
			champion.flag.weapon_flag.jkxq[0] = True
			self.Super_weapon(champion,self.weapon[2]) 
		elif self.weapon[0] + self.weapon[1] in ('暴风大剑钢铁锁甲','钢铁锁甲暴风大剑'):
			self.weapon[2] = '守护天使'
			champion.flag.weapon_flag.shts[0] = True
			champion.flag.weapon_flag.shts[1] = True
		elif self.weapon[0] + self.weapon[1] in ('暴风大剑负极斗篷','负极斗篷暴风大剑'):
			self.weapon[2] = '饮血巨剑'
			champion.flag.weapon_flag.yxjj[0] = True
			champion.champion.hemophagia += champion.flag.weapon_flag.yxjj[1]
		elif self.weapon[0] + self.weapon[1] in ('暴风大剑无用大棒','无用大棒暴风大剑'):
			self.weapon[2] = '科技枪刃'
			champion.flag.weapon_flag.kjqr[0] = True
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('暴风大剑格斗手套','格斗手套暴风大剑'):
			self.weapon[2] = '无尽之刃'
			champion.flag.weapon_flag.wjzr[0] = True
			self.Super_weapon(champion,self.weapon[2])
			champion.champion.attack_attribute.crit_mechanism.Add_crit(champion.flag.weapon_flag.wjzr[1][0])
			champion.champion.attack_attribute.crit_mechanism.crit_multiple += champion.flag.weapon_flag.wjzr[1][1]
		elif self.weapon[0] + self.weapon[1] == '反曲之弓反曲之弓':
			self.weapon[2] = '疾射火炮'
			champion.flag.weapon_flag.jshp[0] = True
			if champion.champion.name == 'Jhin':
				champion.As2cr(1 + champion.flag.weapon_flag.jshp[1][0])
			else:
					champion.champion.attack_attribute.attack_speed *= (1 + champion.flag.weapon_flag.jshp[1][0])
			champion.champion.attack_attribute.crit_mechanism.Add_crit(champion.flag.weapon_flag.jshp[1][1])
		elif self.weapon[0] + self.weapon[1] in ('反曲之弓女神之泪','女神之泪反曲之弓'):
			self.weapon[2] = '狂热电刀'
			champion.flag.weapon_flag.krdd[0] = True
		elif self.weapon[0] + self.weapon[1] in ('反曲之弓巨人腰带','巨人腰带反曲之弓'):
			if version[0] == 1:
				self.weapon[2] = '卑劣手斧'
				champion.flag.weapon_flag.blsf[0] = True
			elif version[0] in (2,3):
				if champion.champion.name in ('Garen','SuperGaren'):
					self.weapon[2] = '巨型九头蛇'
					champion.flag.weapon_flag.jxjts[0] = True
				else:
					self.weapon[2] = '荣光凯旋'
					champion.flag.weapon_flag.rgkx[0] = True
					champion.champion.hp.max_value += champion.flag.weapon_flag.rgkx[1]
					champion.champion.hp.value += champion.flag.weapon_flag.rgkx[1]
		elif self.weapon[0] + self.weapon[1] in ('反曲之弓钢铁锁甲','钢铁锁甲反曲之弓'):
			self.weapon[2] = '幻影之舞'
			champion.flag.weapon_flag.hyzw[0] = True
		elif self.weapon[0] + self.weapon[1] in ('反曲之弓负极斗篷','负极斗篷反曲之弓'):
			self.weapon[2] = '分裂飓风'
			champion.flag.weapon_flag.fljf[0] = True
		elif self.weapon[0] + self.weapon[1] in ('反曲之弓无用大棒','无用大棒反曲之弓'):
			self.weapon[2] = '鬼索之怒'
			champion.flag.weapon_flag.gszn[0] = True
		elif self.weapon[0] + self.weapon[1] in ('反曲之弓格斗手套','格斗手套反曲之弓'):
			self.weapon[2] = '凡性提醒'
			champion.flag.weapon_flag.fxtx[0] = True
			champion.champion.attack_attribute.armor_penetration += champion.flag.weapon_flag.fxtx[1][0]
		elif self.weapon[0] + self.weapon[1] == '女神之泪女神之泪':
			self.weapon[2] = '天使之拥'
			champion.flag.weapon_flag.tszy[0] = True
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('女神之泪巨人腰带','巨人腰带女神之泪'):
			self.weapon[2] = '神圣救赎'
			champion.flag.weapon_flag.ssjs[0] = True
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('女神之泪钢铁锁甲','钢铁锁甲女神之泪'):
			self.weapon[2] = '冰霜之心'
			champion.flag.weapon_flag.bszx[0] = True 
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('女神之泪负极斗篷','负极斗篷女神之泪'):
			self.weapon[2] = '沉默匕首'
			champion.flag.weapon_flag.cmbs[0] = True
		elif self.weapon[0] + self.weapon[1] in ('女神之泪无用大棒','无用大棒女神之泪'):
			self.weapon[2] = '卢登回声'
			champion.flag.weapon_flag.ldhs[0] = True
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('女神之泪格斗手套','格斗手套女神之泪'):
			self.weapon[2] = '正义之手'
			champion.flag.weapon_flag.zyzs[0] = True
		elif self.weapon[0] + self.weapon[1] == '巨人腰带巨人腰带':
			self.weapon[2] = '狂徒铠甲'
			champion.flag.weapon_flag.ktkj[0] = True
		elif self.weapon[0] + self.weapon[1] in ('巨人腰带钢铁锁甲','钢铁锁甲巨人腰带'):
			self.weapon[2] = '泰坦坚决'
			champion.flag.weapon_flag.ttjj[0] = True
		elif self.weapon[0] + self.weapon[1] in ('巨人腰带负极斗篷','负极斗篷巨人腰带'):
			self.weapon[2] = '深渊面具'
			champion.flag.weapon_flag.symj[0] = True
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('巨人腰带无用大棒','无用大棒巨人腰带'):
			self.weapon[2] = '死亡秘典'
			champion.flag.weapon_flag.swmd[0] = True
			champion.champion.attack_attribute.spell_resistance_penetration += champion.flag.weapon_flag.swmd[1][1]
		elif self.weapon[0] + self.weapon[1] in ('巨人腰带格斗手套','格斗手套巨人腰带'):
			self.weapon[2] = '伏击之爪'
			champion.flag.weapon_flag.fjzz[0] = True
		elif self.weapon[0] + self.weapon[1] == '钢铁锁甲钢铁锁甲':
			self.weapon[2] = '荆棘之甲'
			champion.flag.weapon_flag.jjzj[0] = True
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('钢铁锁甲负极斗篷','负极斗篷钢铁锁甲'):
			self.weapon[2] = '折戟秘刀'
			champion.flag.weapon_flag.zjmd[0] = True
		elif self.weapon[0] + self.weapon[1] in ('钢铁锁甲无用大棒','无用大棒钢铁锁甲'):
			self.weapon[2] = '烈阳之匣'
			champion.flag.weapon_flag.lyzx[0] = True
			self.Super_weapon(champion,self.weapon[2])
			numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
			num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
			for i in range(3):
				if not champion.flag.special_flag.dead_area[0]:
					if numTF[i] and (not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag) and (not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.miss_flag[0])\
					and (not champion.game.LR[champion.position][num_pos[i]].flag.special_flag.dead_area[0]):
						champion.game.LR[champion.position][num_pos[i]].condition.shield.Add_shield(champion.game.LR[champion.position][num_pos[i]],champion.flag.weapon_flag.lyzx[1][0],champion.flag.weapon_flag.lyzx[1][1])
				else:
					champion.condition.shield.Add_shield(champion,champion.flag.weapon_flag.lyzx[1][0],champion.flag.weapon_flag.lyzx[1][1])
		elif self.weapon[0] + self.weapon[1] in ('钢铁锁甲格斗手套','格斗手套钢铁锁甲'):
			if version[0] in (1,2):
				self.weapon[2] = '冰脉护手'
				champion.flag.weapon_flag.bmhs[0] = True
				champion.champion.defensive_attribute.dodge_mechanism.Add_dodge(champion.flag.weapon_flag.bmhs[1][0])
			elif version[0] == 3:
				self.weapon[2] = '静止法衣'
				champion.flag.weapon_flag.jzfy[0] = True
				champion.flag.weapon_flag.jzfy[1] = True
				if not champion.game.LR[~champion.position+2][champion.pos_num].flag.condition_flag.death_flag and not champion.game.LR[~champion.position+2][champion.pos_num].flag.condition_flag.miss_flag[0] \
				and not champion.game.LR[~champion.position+2][champion.pos_num].flag.condition_flag.buff_invincible_flag:
					champion.condition.broken.Add_brokrn(champion.game.LR[~champion.position+2][champion.pos_num])
		elif self.weapon[0] + self.weapon[1] == '负极斗篷负极斗篷':
			self.weapon[2] = '巨龙之牙'
			champion.flag.weapon_flag.jlzy[0] = True
			self.Super_weapon(champion,self.weapon[2])
		elif self.weapon[0] + self.weapon[1] in ('负极斗篷无用大棒','无用大棒负极斗篷'):
			self.weapon[2] = '离子火花'
			champion.flag.weapon_flag.lzhh[0] = True
		elif self.weapon[0] + self.weapon[1] in ('负极斗篷格斗手套','格斗手套负极斗篷'):
			self.weapon[2] = '水银披风'
			champion.flag.weapon_flag.sypf[0] = True
			champion.flag.weapon_flag.sypf[2] = True
			if not champion.champion.name == 'AurelionSol':
				champion.condition.unstoppable.Add_unstoppable(champion,champion.flag.weapon_flag.sypf[1])
		elif self.weapon[0] + self.weapon[1] == '无用大棒无用大棒':
			self.weapon[2] = '灭世之帽'
			champion.flag.weapon_flag.mszm[0] = True
			self.Super_weapon(champion,self.weapon[2])
			if champion.champion.name == 'Heimerdinger':
				champion.Add_spell_power(champion.flag.weapon_flag.mszm[1])
			else:
				champion.champion.attack_attribute.spell_power += champion.flag.weapon_flag.mszm[1]
		elif self.weapon[0] + self.weapon[1] in ('无用大棒格斗手套','格斗手套无用大棒'):
			self.weapon[2] = '珠光拳套'
			champion.flag.weapon_flag.zgqt[0] = True
			champion.champion.attack_attribute.crit_mechanism.Add_crit(champion.flag.weapon_flag.zgqt[4])
		elif self.weapon[0] + self.weapon[1] == '格斗手套格斗手套':
			self.weapon[2] = '窃贼手套'
			champion.flag.weapon_flag.qzst = True
			for i in range(3):
				champion.weapon.weapon[3+i] = basic_weapon.get(randint(1, 9))
				champion.weapon.Equip_weapon(4+i,champion)
		elif self.weapon[0] + self.weapon[1] in ('金色魔铲暴风大剑','暴风大剑金色魔铲'):
			if version[0] in (1,3):
				if version[0] == 1:
					self.weapon[2] = '夜袭暮刃'
					champion.flag.weapon_flag.yxmr[0] = True
					champion.champion.attack_attribute.armor_penetration += champion.flag.weapon_flag.yxmr[1]
				elif version[0] == 3:
					self.weapon[2] = '夜之锋刃'
					champion.flag.weapon_flag.yzfr[0] = True
					champion.champion.attack_attribute.armor_penetration += champion.flag.weapon_flag.yzfr[1]
					champion.flag.weapon_flag.yzfr[3][0].value = 500
				if champion.champion.relatedness.profession[0] != '刺客':
					champion.champion.relatedness.extra[0] = '刺客'
					champion.champion.attack_attribute.armor_penetration += 15
					champion.champion.attack_attribute.spell_resistance_penetration += 15
					champion.game.LR_rela[champion.position]['刺客'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['刺客'] > 1:
						champion.champion.attack_attribute.crit_mechanism.crit += rela_dic['刺客'][1][champion.game.LR_rela[champion.position]['刺客'] - 2][0]
						champion.champion.attack_attribute.crit_mechanism.crit_multiple += rela_dic['刺客'][1][champion.game.LR_rela[champion.position]['刺客'] - 2][1]
						for i in range(3):
							if (champion.friend[i].champion.relatedness.profession[0] == '刺客' or champion.friend[i].champion.relatedness.extra[0] == '刺客')\
							 and (champion.friend[i] != champion) and (not champion.friend[i].flag.condition_flag.death_flag):
								champion.friend[i].champion.attack_attribute.crit_mechanism.crit += rela_dic['刺客'][1][0][0]
								champion.friend[i].champion.attack_attribute.crit_mechanism.crit_multiple += rela_dic['刺客'][1][0][1]
			elif version[0] == 2:
				self.weapon[2] = '樱手里剑'
				champion.flag.weapon_flag.yslj[0] = True
				# 加能量
				champion.champion.mp.Calculation(champion,champion.flag.weapon_flag.yslj[1])
				if champion.champion.relatedness.profession[0] not in ('忍者','忍剑士'):
					champion.champion.relatedness.extra[0] = '忍者'
					# 法力机制转能量机制
					champion.flag.special_flag.chakra_flag = True
					#	clean中毒、沉默、朔极之矛
					champion.condition.poisoning.Clean(champion.flag)
					champion.condition.silence.Clean(champion.flag)
					champion.flag.weapon_flag.sjzm[1] = False

					champion.game.LR_rela[champion.position]['忍者'] += 1
					champion.game.Rela_record()
					# 忍者buff
					if champion.game.LR_rela[champion.position]['忍者'] > 1:
						champion.game.Ninja_buff(champion,rela_dic['忍者'][1][(champion.game.LR_rela[champion.position]['忍者'] - 2)])

		elif self.weapon[0] + self.weapon[1] in ('金色魔铲反曲之弓','反曲之弓金色魔铲'):
			if version[0] == 1:
				self.weapon[2] = '神臂之弓'
				champion.flag.weapon_flag.sbzg[0] = True
				champion.champion.attack_attribute.attack_speed *= (1 + champion.flag.weapon_flag.sbzg[4])
				if champion.champion.relatedness.profession[0] != '游侠':
					champion.champion.relatedness.extra[0] = '游侠'
					champion.game.LR_rela[champion.position]['游侠'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['游侠'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.profession[0] == '游侠' or champion.friend[i].champion.relatedness.extra[0] == '游侠':
								champion.friend[i].flag.rela_flag['游侠'][0] = True
								champion.friend[i].flag.rela_flag['游侠'][1] = rela_dic['游侠'][1][champion.game.LR_rela[champion.position]['游侠'] - 2]
			elif version[0] in (2,3):
				self.weapon[2] = '破败王者'
				champion.flag.weapon_flag.pbwz[0] = True
				if champion.champion.relatedness.profession[0] not in ('剑士','忍剑士'):
					champion.champion.relatedness.extra[0] = '剑士'
					champion.game.LR_rela[champion.position]['剑士'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['剑士'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.profession[0] == '剑士' or champion.friend[i].champion.relatedness.extra[0] == '剑士':
								champion.friend[i].flag.rela_flag['剑士'][0] = True
								champion.friend[i].flag.rela_flag['剑士'][1] = rela_dic['剑士'][1][champion.game.LR_rela[champion.position]['剑士'] - 2]
		elif self.weapon[0] + self.weapon[1] in ('金色魔铲女神之泪','女神之泪金色魔铲'):
			if version[0] in (1,2):
				self.weapon[2] = '巫师法帽'
				champion.flag.weapon_flag.wsfm[0] = True
				champion.flag.weapon_flag.wsfm[2][0] = True
				if champion.champion.relatedness.profession[0] != '法师':
					champion.champion.relatedness.extra[0] = '法师'
					champion.game.LR_rela[champion.position]['法师'] += 1
					champion.game.Rela_record()
					champion.champion.mp.basic_MP_restore = champion.flag.weapon_flag.wsfm[1]
					if champion.game.LR_rela[champion.position]['法师'] > 1:
						champion.champion.attack_attribute.spell_power += rela_dic['法师'][1][champion.game.LR_rela[champion.position]['法师'] - 2]
						for i in range(3):
							if (champion.friend[i].champion.relatedness.profession[0] == '法师' or champion.friend[i].champion.relatedness.extra[0] == '法师')\
							 and (champion.friend[i] != champion) and (not champion.friend[i].flag.condition_flag.death_flag):
								champion.friend[i].champion.attack_attribute.spell_power += rela_dic['法师'][1][0]
			elif version[0] == 3:
				self.weapon[2] = '魅惑挂坠'
				champion.flag.weapon_flag.mhgz[0] = True
				if champion.champion.relatedness.element[0] != '星之守护者':
					champion.champion.relatedness.extra[0] = '星之守护者'
					champion.game.LR_rela[champion.position]['星之守护者'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['星之守护者'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] == '星之守护者' or champion.friend[i].champion.relatedness.extra[0] == '星之守护者':
								champion.friend[i].flag.rela_flag['星之守护者'][0] = True
								champion.friend[i].flag.rela_flag['星之守护者'][1] = rela_dic['星之守护者'][1][champion.game.LR_rela[champion.position]['星之守护者'] - 2]
		elif self.weapon[0] + self.weapon[1] in ('金色魔铲巨人腰带','巨人腰带金色魔铲'):
			if version[0] in (1,2): 
				self.weapon[2] = '极地战锤'
				champion.flag.weapon_flag.jdzc[0] = True
				if champion.champion.relatedness.element[0] != '极地':
					champion.champion.relatedness.extra[0] = '极地'
					champion.game.LR_rela[champion.position]['极地'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['极地'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] == '极地' or champion.friend[i].champion.relatedness.extra[0] == '极地':
								champion.friend[i].flag.rela_flag['极地'][0] = True
								champion.friend[i].flag.rela_flag['极地'][1] = rela_dic['极地'][1][champion.game.LR_rela[champion.position]['极地'] - 2]
			elif version[0] == 3:
				self.weapon[2] = '淬炼勋章'
				champion.flag.weapon_flag.clxz[0] = True
				if champion.champion.relatedness.element[0] != '奥德赛':
					champion.champion.relatedness.extra[0] = '奥德赛'
					champion.game.LR_rela[champion.position]['奥德赛'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['奥德赛'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] == '奥德赛' or champion.friend[i].champion.relatedness.extra[0] == '奥德赛':
								champion.friend[i].flag.rela_flag['奥德赛'][0] = True
								champion.friend[i].flag.rela_flag['奥德赛'][1] = rela_dic['奥德赛'][1][champion.game.LR_rela[champion.position]['奥德赛'] - 2]
						champion.champion.relatedness.Odyssey(champion.game,champion.position,1,champion)
		elif self.weapon[0] + self.weapon[1] in ('金色魔铲钢铁锁甲','钢铁锁甲金色魔铲'):
			if version[0] in (1,2):
				self.weapon[2] = '巨石板甲'
				champion.flag.weapon_flag.jsbj[0] = True
				if champion.champion.relatedness.profession[0] != '守护神':
					champion.champion.relatedness.extra[0] = '守护神'
					champion.game.LR_rela[champion.position]['守护神'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['守护神'] > 1:
						champion.champion.defensive_attribute.armor += rela_dic['守护神'][1][champion.game.LR_rela[champion.position]['守护神'] - 2]
						for i in range(3):
							if (champion.friend[i].champion.relatedness.profession[0] == '守护神' or champion.friend[i].champion.relatedness.extra[0] == '守护神')\
							 and (champion.friend[i] != champion) and (not champion.friend[i].flag.condition_flag.death_flag):
								champion.friend[i].champion.defensive_attribute.armor += rela_dic['守护神'][1][0]
			elif version[0] == 3:
				self.weapon[2] = '圣银胸甲'
				champion.flag.weapon_flag.syxj[0] = True
				if champion.champion.relatedness.profession[0] != '护卫':
					champion.champion.relatedness.extra[0] = '护卫'
					champion.game.LR_rela[champion.position]['护卫'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['护卫'] == 2:
						for i in range(3):
							if (champion.friend[i].champion.relatedness.profession[0] == '护卫' or champion.friend[i].champion.relatedness.extra[0] == '护卫'):
								champion.friend[i].champion.defensive_attribute.armor += rela_dic['护卫'][1][0][0]
								numTF = [champion.friend[i].pos_num - 1 >= 0, champion.friend[i].pos_num + 1 <= 2]
								num_pos = [champion.friend[i].pos_num - 1, champion.friend[i].pos_num + 1]
								champion.friend[i].flag.rela_flag['护卫'][2][0] = True
								for j in range(2):
									if numTF[j]:
										if not champion.game.LR[champion.position][num_pos[j]].flag.condition_flag.death_flag:
											champion.game.LR[champion.position][num_pos[j]].champion.defensive_attribute.armor += rela_dic['护卫'][1][0][1]
					elif champion.game.LR_rela[champion.position]['护卫'] == 3:
						champion.champion.defensive_attribute.armor += rela_dic['护卫'][1][1][0]
						numTF = [champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
						num_pos = [champion.pos_num - 1, champion.pos_num + 1]
						champion.flag.rela_flag['护卫'][2][0] = True
						for i in range(2):
							if numTF[i]:
								if not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag:
									champion.game.LR[champion.position][num_pos[i]].champion.defensive_attribute.armor += rela_dic['护卫'][1][1][1]
						for i in range(3):
							if (champion.friend[i].champion.relatedness.profession[0] == '护卫' or champion.friend[i].champion.relatedness.extra[0] == '护卫')\
							 and (champion.friend[i] != champion):
								champion.friend[i].flag.rela_flag['护卫'][2][0] = True
								champion.friend[i].champion.defensive_attribute.armor += rela_dic['护卫'][1][0][0]
								numTF = [champion.friend[i].pos_num - 1 >= 0, champion.friend[i].pos_num + 1 <= 2]
								num_pos = [champion.friend[i].pos_num - 1, champion.friend[i].pos_num + 1]
								for j in range(2):
									if numTF[j]:
										if not champion.game.LR[champion.position][num_pos[j]].flag.condition_flag.death_flag:
											champion.game.LR[champion.position][num_pos[j]].champion.defensive_attribute.armor += rela_dic['护卫'][1][0][1]
		elif self.weapon[0] + self.weapon[1] in ('金色魔铲负极斗篷','负极斗篷金色魔铲'):
			if version[0] in (1,2):
				self.weapon[2] = '炽热香炉'
				champion.flag.weapon_flag.crxl[0] = True
				if champion.champion.relatedness.profession[0] != '秘术师':
					champion.champion.relatedness.extra[0] = '秘术师'
					champion.game.LR_rela[champion.position]['秘术师'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['秘术师'] > 1:
						champion.champion.defensive_attribute.spell_resistance += rela_dic['秘术师'][1][champion.game.LR_rela[champion.position]['秘术师'] - 2]
						for i in range(3):
							if  (champion.friend[i] != champion) and (not champion.friend[i].flag.condition_flag.death_flag):
								champion.friend[i].champion.defensive_attribute.spell_resistance += rela_dic['秘术师'][1][0]
			elif version[0] == 3:
				self.weapon[2] = '星神法球'
				champion.flag.weapon_flag.xsfq[0] = True
				if champion.champion.relatedness.element[0] != '星神':
					champion.champion.relatedness.extra[0] = '星神'
					champion.game.LR_rela[champion.position]['星神'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['星神'] > 1:
						for i in range(3):
							champion.friend[i].flag.rela_flag['星神'][3] = True
							champion.friend[i].flag.rela_flag['星神'][1] = rela_dic['星神'][1][champion.game.LR_rela[champion.position]['星神'] - 2]
							if champion.friend[i].champion.relatedness.element[0] == '星神' or champion.friend[i].champion.relatedness.extra[0] == '星神':
								champion.friend[i].flag.rela_flag['星神'][0] = True
		elif self.weapon[0] + self.weapon[1] in ('金色魔铲无用大棒','无用大棒金色魔铲'):
			if version[0] == 1:
				self.weapon[2] = '斑比熔渣'
				champion.flag.weapon_flag.bbrz[0] = True
				if champion.champion.relatedness.element[0] not in ('地狱火','黯焰'):
					champion.champion.relatedness.extra[0] = '地狱火'
					champion.game.LR_rela[champion.position]['地狱火'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['地狱火'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] in ('地狱火','黯焰') or champion.friend[i].champion.relatedness.extra[0] == '地狱火':
								champion.friend[i].flag.rela_flag['地狱火'][0] = True
								champion.friend[i].flag.rela_flag['地狱火'][1] = rela_dic['地狱火'][1][champion.game.LR_rela[champion.position]['地狱火'] - 2]
			elif version[0] == 2:
				self.weapon[2] = '暗影核心'
				champion.flag.weapon_flag.ayhx[0] = True
				champion.flag.weapon_flag.ayhx[1][0] = True
				if champion.champion.relatedness.element[0] != '影':
					champion.champion.relatedness.extra[0] = '影'
					champion.game.LR_rela[champion.position]['影'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['影'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] == '影' or champion.friend[i].champion.relatedness.extra[0] == '影':
								champion.friend[i].flag.rela_flag['影'][0] = True
								champion.friend[i].flag.rela_flag['影'][1] = rela_dic['影'][1][champion.game.LR_rela[champion.position]['影'] - 2]
			elif version[0] == 3:
				self.weapon[2] = '爆破炸弹'
				champion.flag.weapon_flag.bpzd[0] = True
				if champion.champion.relatedness.profession[0] != '爆破专家':
					champion.champion.relatedness.extra[0] = '爆破专家'
					champion.game.LR_rela[champion.position]['爆破专家'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['爆破专家'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.profession[0] == '爆破专家' or champion.friend[i].champion.relatedness.extra[0] == '爆破专家':
								champion.friend[i].flag.rela_flag['爆破专家'][0] = True
								champion.friend[i].flag.rela_flag['爆破专家'][1] = rela_dic['爆破专家'][1][champion.game.LR_rela[champion.position]['爆破专家'] - 2]
		elif self.weapon[0] + self.weapon[1] in ('金色魔铲格斗手套','格斗手套金色魔铲'):
			if version[0] == 1:
				self.weapon[2] = '黑暗切割'
				champion.flag.weapon_flag.haqg[0] = True
				if champion.champion.relatedness.profession[0] != '狂战士':
					champion.champion.relatedness.extra[0] = '狂战士'
					champion.game.LR_rela[champion.position]['狂战士'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['狂战士'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.profession[0] == '狂战士' or champion.friend[i].champion.relatedness.extra[0] == '狂战士':
								champion.friend[i].flag.rela_flag['狂战士'][0] = True
								champion.friend[i].flag.rela_flag['狂战士'][1] = rela_dic['狂战士'][1][champion.game.LR_rela[champion.position]['狂战士'] - 2]
					if champion.game.LR_rela[champion.position]['狂战士'] == 3:
						for j in range(3):
							champion.friend[j].champion.attack_attribute.AD += rela_dic['狂战士'][1][3]
			elif version[0] == 2:
				self.weapon[2] = '雷霆劫掠'
				champion.flag.weapon_flag.ltjl[0] = True
				if champion.champion.relatedness.element[0] != '雷霆':
					champion.champion.relatedness.extra[0] = '雷霆'
					champion.game.LR_rela[champion.position]['雷霆'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['雷霆'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] == '雷霆' or champion.friend[i].champion.relatedness.extra[0] == '雷霆':
								champion.friend[i].flag.rela_flag['雷霆'][0] = True
								champion.friend[i].flag.rela_flag['雷霆'][1] = rela_dic['雷霆'][1][champion.game.LR_rela[champion.position]['雷霆'] - 2]
			elif version[0] == 3:
				self.weapon[2] = '黑暗之心'
				champion.flag.weapon_flag.hazx[0] = True
				if champion.champion.relatedness.element[0] != '暗星':
					champion.champion.relatedness.extra[0] = '暗星'
					champion.game.LR_rela[champion.position]['暗星'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['暗星'] > 1:	
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] == '暗星' or champion.friend[i].champion.relatedness.extra[0] == '暗星':
								champion.friend[i].flag.rela_flag['暗星'][0] = True
								champion.friend[i].flag.rela_flag['暗星'][1] = rela_dic['暗星'][1][champion.game.LR_rela[champion.position]['暗星'] - 2]
		elif self.weapon[0] + self.weapon[1] == '金色魔铲金色魔铲':
			if version[0] == 1:
				self.weapon[2] = '飞升护符'
				champion.flag.weapon_flag.fshf[0] = True
				if champion.champion.relatedness.element[0] != '光':
					champion.champion.relatedness.extra[0] = '光'
					champion.game.LR_rela[champion.position]['光'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['光'] > 1:
						for i in range(3):
							if champion.friend[i].champion.relatedness.element[0] == '光' or champion.friend[i].champion.relatedness.extra[0] == '光':
								champion.friend[i].flag.rela_flag['光'][0] = True
								champion.friend[i].flag.rela_flag['光'][1] = rela_dic['光'][1][champion.game.LR_rela[champion.position]['光'] - 2]
			elif version[0] == 2:
				self.weapon[2] = '清风之灵'
				champion.flag.weapon_flag.qfzl[0] = True
				if champion.champion.relatedness.element[0] != '云霄':
					champion.champion.relatedness.extra[0] = '云霄'
					champion.game.LR_rela[champion.position]['云霄'] += 1
					champion.game.Rela_record()
					if champion.game.LR_rela[champion.position]['云霄'] > 1:
						champion.champion.defensive_attribute.dodge_mechanism.Add_dodge(rela_dic['云霄'][1][champion.game.LR_rela[champion.position]['云霄'] - 2])
						for i in range(3):
							if  (champion.friend[i] != champion) and (not champion.friend[i].flag.condition_flag.death_flag):
								champion.friend[i].champion.defensive_attribute.dodge_mechanism.Add_dodge(rela_dic['云霄'][1][0])
			elif version[0] == 3:
				self.weapon[2] = '虚空之门'
				champion.flag.weapon_flag.xkzm[0] = True

	# 武器效果代码

	# 狂徒铠甲效果
	def Ktjk(self,champion):
		champion.flag.weapon_flag.ktkj[1] += 1
		if champion.flag.weapon_flag.ktkj[1] >= 100 / time_correction[0]:
			hp_restore_value = int(champion.flag.weapon_flag.ktkj[2] * (champion.champion.hp.max_value - champion.champion.hp.value))
			if hp_restore_value > champion.flag.weapon_flag.ktkj[3]:
				hp_restore_value = champion.flag.weapon_flag.ktkj[3]
			champion.champion.hp.HP_restore(hp_restore_value,champion.champion,champion)
			champion.flag.weapon_flag.ktkj[1] = 0
	# 神圣救赎效果
	def Ssjs(self,champion):
		end_flag = champion.flag.weapon_flag.ssjs[4][1].Duration(champion.flag.weapon_flag.ssjs[4][2])
		if end_flag:
			numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
			num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]	
			# 治疗
			if not champion.flag.special_flag.dead_area[0]:
				for i in range(3):
					if numTF[i] and (not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag) and (not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.miss_flag[0])\
					and (not champion.game.LR[champion.position][num_pos[i]].flag.special_flag.dead_area[0]):
						champion.game.LR[champion.position][num_pos[i]].champion.hp.HP_restore(champion.flag.weapon_flag.ssjs[2],champion.champion,champion.game.LR[champion.position][num_pos[i]])
			else:
				champion.champion.hp.HP_restore(champion.flag.weapon_flag.ssjs[2],champion.champion,champion)
			champion.flag.weapon_flag.ssjs[4][0] = False
			champion.flag.weapon_flag.ssjs[1] = False
	# 卢登回声效果
	def Ldhs(self,champion,enemy):
		if not champion.flag.special_flag.dead_area[0] or champion.champion.name == 'Mordekaiser':
			numTF = [enemy.pos_num - 1 >= 0, enemy.pos_num + 1 <= 2]
			num_pos = [enemy.pos_num - 1, enemy.pos_num +1]
			enemy_temp = champion.enemy
			for i in range(2):
				if numTF[i] and (not champion.game.LR[enemy.position][num_pos[i]].flag.condition_flag.death_flag) and (not champion.game.LR[enemy.position][num_pos[i]].flag.condition_flag.miss_flag[0])\
				and (not champion.game.LR[enemy.position][num_pos[i]].flag.special_flag.dead_area[0]):
							champion.champion.attack_attribute.spell_attack.physical_damage = 0
							champion.champion.attack_attribute.spell_attack.spell_damage = champion.flag.weapon_flag.ldhs[3]
							champion.champion.attack_attribute.spell_attack.real_damage = 0
							champion.enemy = champion.game.LR[enemy.position][num_pos[i]]
							# 伤害计算
							champion.Spell_attack_damage_calculation()
							champion.enemy.flag.special_flag.effect['卢登回声'][0] = True
			champion.enemy = enemy_temp
		champion.flag.weapon_flag.ldhs[1] = False
	# 守护天使效果
	def Shts(self,champion):
		# 清除除重伤意外的状态
		champion.condition.Clean_condition(champion,1)
		champion.condition.miss.Add_miss(champion, champion.flag.weapon_flag.shts[4])
		champion.flag.weapon_flag.shts[1] = False
		champion.flag.weapon_flag.shts[2] = True
		# 恢复血量的代码写在"不可选取状态处理"中
	# 巫师法帽效果
	def Wsfm(self,champion):
		champion.champion.hp.value = champion.flag.weapon_flag.wsfm[2][1]
		champion.condition.miss.Add_miss(champion, champion.flag.weapon_flag.wsfm[2][2])
		champion.flag.weapon_flag.wsfm[2][0] = False
		champion.flag.weapon_flag.wsfm[3] = True
	# 分裂飓风效果
	def Fljf(self,champion):
		# 判断额外目标
		enemy = champion.enemy
		if not champion.flag.special_flag.dead_area[0]:
			if (champion.enemy.pos_num - 1 >= 0) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1].flag.condition_flag.death_flag) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1].flag.condition_flag.miss_flag[0])\
			and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1].flag.special_flag.dead_area[0]):
				champion.flag.weapon_flag.fljf[3] = '额外目标:%s' % champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1].champion.name
				champion.enemy = champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1]
			elif (champion.enemy.pos_num + 1 <= 2) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1].flag.condition_flag.death_flag) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1].flag.condition_flag.miss_flag[0])\
			and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1].flag.special_flag.dead_area[0]):
				champion.flag.weapon_flag.fljf[3] = '额外目标:%s' % champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1].champion.name
				champion.enemy = champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1]
			else:
				champion.flag.weapon_flag.fljf[3] = '额外目标：无'
		else:
			champion.flag.weapon_flag.fljf[3] = '额外目标：无'
		# 飓风伤害计算
		if champion.enemy != enemy:
			# 敌人闪避判断
			dodge_flag = champion.champion.defensive_attribute.dodge_mechanism.Dodge_judg(champion.enemy) \
			and (not champion.enemy.flag.condition_flag.debuff_dizz_flag) and (not champion.enemy.flag.condition_flag.debuff_frozen_flag)
			if dodge_flag:
				champion.champion.attack_attribute.normal_attack_damage.total_damage = 0
				if champion.enemy.flag.weapon_flag.fshf[0]: 				# 触发飞升护符效果(敌人)
					champion.weapon.Fshf(champion)
				elif champion.enemy.flag.weapon_flag.qfzl[0]: 				# 触发清风之灵效果(敌人)
					champion.weapon.Qfzl(champion)
				# 触发敌人冰脉护手效果
				elif champion.enemy.flag.weapon_flag.bmhs[0]: 				
					champion.weapon.Bmhs(champion)
			else:
				# 复制普攻伤害原值
				champion.champion.attack_attribute.normal_attack.physical_damage = champion.champion.attack_attribute.normal_attack_orig.physical_damage
				champion.champion.attack_attribute.normal_attack.spell_damage = champion.champion.attack_attribute.normal_attack_orig.spell_damage
				champion.champion.attack_attribute.normal_attack.real_damage = champion.champion.attack_attribute.normal_attack_orig.real_damage
				champion.flag.weapon_flag.fljf[1] = True   
				champion.Normal_attack_damage_calculation()
				champion.flag.weapon_flag.fljf[1] = False
				# 普攻后计算回蓝
				champion.champion.mp.MP_restore_1(champion.flag, champion, champion.enemy)
		champion.enemy = enemy
		champion.flag.weapon_flag.fljf[2] = False
	# 离子火花效果
	def Lzhh(self,champion):
		if not champion.flag.special_flag.dead_area[0]:
			for i in range(3):						
				if (not champion.game.LR[~champion.position+2][i].flag.condition_flag.death_flag) and (not champion.game.LR[~champion.position+2][i].flag.condition_flag.miss_flag[0]) \
				and (not champion.game.LR[~champion.position+2][i].flag.special_flag.dead_area[0]) and champion.game.LR[~champion.position+2][i].flag.weapon_flag.lzhh[0]:
					self.Lzhh_deal(champion,champion.game.LR[~champion.position+2][i])		 
		else:
			if champion.flag.special_flag.dead_area[1].flag.weapon_flag.lzhh[0] and not champion.flag.special_flag.dead_area[1].flag.condition_flag.miss_flag[0]:
				self.Lzhh_deal(champion,champion.flag.special_flag.dead_area[1])
	# 离子火花效果处理
	def Lzhh_deal(self,champion,enemy):
		# 处理魔法护盾
		if champion.flag.condition_flag.buff_magic_shield_flag:
			champion.flag.condition_flag.buff_magic_shield_flag = False
		elif champion.flag.condition_flag.buff_invincible_flag:
			pass
		else:
			lzhh_damage = champion.champion.mp.max_value * champion.condition.iron.value
			if lzhh_damage > enemy.flag.weapon_flag.lzhh[2]:
				lzhh_damage = enemy.flag.weapon_flag.lzhh[2]
			# 触发水晶羁绊
			if champion.flag.rela_flag['水晶'][0]:
				lzhh_damage = champion.champion.relatedness.Crystal(champion,lzhh_damage)
			# 扣血、击杀判断
			champion.champion.hp.HP_reduce(lzhh_damage,enemy,champion)
			champion.flag.special_flag.effect['离子火花'][0] = True
			# 触发雷霆羁绊(敌人)
			if enemy.flag.rela_flag['雷霆'][0] and lzhh_damage > 0:
				champion.champion.relatedness.Thunder(enemy)
			# 累计造成伤害(敌人)
			enemy.champion.attack_attribute.all_damage.real_damage += lzhh_damage
			enemy.champion.attack_attribute.all_damage.Total_damage_calculation()
		enemy.flag.weapon_flag.lzhh[1] = True  # 显示离子火花触发
		enemy.flag.weapon_flag.lzhh[3] += 1
	# 狂热电刀效果
	def Krdd(self,champion):
		champion.flag.weapon_flag.krdd[1] += 1
		if champion.flag.weapon_flag.krdd[1] >= 3:
			champion.flag.weapon_flag.krdd[1] = 0
			champion.flag.weapon_flag.krdd[3] = True
			champion.flag.weapon_flag.krdd[4] += 1
			# 中心敌人
			if not champion.enemy.flag.condition_flag.miss_flag[0]:
				self.Krdd_deal(champion,champion.enemy)
				champion.enemy.flag.special_flag.effect['狂热电刀'][0] = True
			if not champion.flag.special_flag.dead_area[0]:
				# 两边敌人(判断是否连线)
				# 中心往上
				for i in range(2):
					if (champion.enemy.pos_num - 1 - i >= 0) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1 - i].flag.condition_flag.death_flag) \
					and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1 - i].flag.condition_flag.miss_flag[0]) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1 - i].flag.special_flag.dead_area[0]):
						self.Krdd_deal(champion,champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1 - i])
						champion.game.LR[~champion.position+2][champion.enemy.pos_num - 1 - i].flag.special_flag.effect['狂热电刀'][0] = True
					else:
						break
				# 中心往下
				for i in range(2):
					if (champion.enemy.pos_num + 1 + i <= 2) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1 + i].flag.condition_flag.death_flag) \
					and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1 + i].flag.condition_flag.miss_flag[0]) and (not champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1 + i].flag.special_flag.dead_area[0]):
						self.Krdd_deal(champion,champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1 + i])
						champion.game.LR[~champion.position+2][champion.enemy.pos_num + 1 + i].flag.special_flag.effect['狂热电刀'][0] = True
					else:
						break
	# 狂热电刀伤害计算
	def Krdd_deal(self,champion,enemy):
		# 判断敌人的魔法护盾
		if enemy.flag.condition_flag.buff_magic_shield_flag:
			enemy.flag.condition_flag.buff_magic_shield_flag = False
		elif enemy.flag.condition_flag.buff_invincible_flag:
			pass
		else:
			if enemy.flag.weapon_flag.symj[1]: 											# 触发深渊面具效果
				enemy.flag.weapon_flag.symj[2] = 1 + enemy.flag.weapon_flag.symj[3]
			krdd_damage = (champion.flag.weapon_flag.krdd[2] * (100 / (100 + (enemy.champion.defensive_attribute.spell_resistance \
				* ((1 - champion.champion.attack_attribute.spell_resistance_penetration/100)))))) * enemy.flag.weapon_flag.symj[2] * enemy.condition.matigation.value * enemy.condition.iron.value
			if enemy.flag.weapon_flag.jlzy[0]: 											# 触发敌人的巨龙之牙效果
				krdd_damage *= (1 - enemy.flag.weapon_flag.jlzy[1])
			# 卡萨丁贤者之石被动
			if enemy.champion.name == 'Kassadin':
				champion.champion.attack_attribute.spell_attack_damage.spell_damage *= (1 - enemy.champion.skill.para[3])
			# 触发敌人的水晶羁绊
			if enemy.flag.rela_flag['水晶'][0]:
				krdd_damage = champion.champion.relatedness.Crystal(enemy,krdd_damage)
			# 扣血、击杀判断、累计造成伤害
			enemy.champion.hp.HP_reduce(krdd_damage,champion,enemy)
			champion.champion.attack_attribute.all_damage.spell_damage += krdd_damage
			champion.champion.attack_attribute.all_damage.Total_damage_calculation()
			# 触发雷霆羁绊
			if champion.flag.rela_flag['雷霆'][0] and krdd_damage > 0:
				champion.champion.relatedness.Thunder(champion)
	# 荆棘之甲效果
	def Jjzj(self,champion,crit_multiple):
		# 反弹伤害计算
		rebound_damage = ((champion.champion.attack_attribute.normal_attack.physical_damage \
			+ champion.champion.attack_attribute.normal_attack.spell_damage * champion.enemy.flag.weapon_flag.symj[2] \
			+ champion.champion.attack_attribute.normal_attack.real_damage) * crit_multiple\
			- champion.champion.attack_attribute.normal_attack_damage.total_damage) * champion.condition.iron.value \
			* champion.enemy.flag.weapon_flag.jjzj[1][0]
		# 触发水晶羁绊
		if champion.flag.rela_flag['水晶'][0]:
			rebound_damage = champion.champion.relatedness.Crystal(champion,rebound_damage)
		# 计算扣血、判断击杀
		champion.champion.hp.HP_reduce(rebound_damage,champion.enemy,champion)
		# 荆棘之甲重伤效果
		champion.condition.injury.Add_injury(champion, champion.enemy.flag.weapon_flag.jjzj[1][1])
		# 累计造成伤害(敌人)
		champion.enemy.champion.attack_attribute.all_damage.real_damage += rebound_damage
		champion.enemy.champion.attack_attribute.all_damage.Total_damage_calculation()
		# 触发雷霆羁绊(敌人)
		if champion.enemy.flag.rela_flag['雷霆'][0] and rebound_damage > 0:
			champion.champion.relatedness.Thunder(champion.enemy)
	# 冰脉护手效果
	def Bmhs(self,champion):
		numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
		num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
		if not champion.flag.special_flag.dead_area[0]:
			for i in range(3):
				if numTF[i]:
					if not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag and not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.miss_flag[0] \
					and not champion.game.LR[champion.position][num_pos[i]].flag.special_flag.dead_area[0] and not champion.game.LR[champion.position][num_pos[i]].flag.special_flag.Nabasre_flag:
						if champion.game.LR[champion.position][num_pos[i]].champion.name == 'Jhin':
							champion.game.LR[champion.position][num_pos[i]].As2cr(1 - champion.enemy.flag.weapon_flag.bmhs[1][1])
						else:
							champion.game.LR[champion.position][num_pos[i]].champion.attack_attribute.attack_speed *= (1 - champion.enemy.flag.weapon_flag.bmhs[1][1])
						champion.game.LR[champion.position][num_pos[i]].flag.special_flag.effect['冰脉护手'][0] = True
		else:
			if not champion.flag.special_flag.Nabasre_flag:
				champion.champion.attack_attribute.attack_speed *= (1 - champion.enemy.flag.weapon_flag.bmhs[1][1])
		champion.enemy.flag.weapon_flag.bmhs[2] = True
		champion.enemy.flag.weapon_flag.bmhs[3] += 1
	# 飞升护符效果
	def Fshf(self,champion):
		champion.enemy.champion.attack_attribute.attack_speed *= (1 + champion.enemy.flag.weapon_flag.fshf[1])
		champion.enemy.flag.weapon_flag.fshf[2] = True
		champion.enemy.flag.weapon_flag.fshf[3] += 1
	# 清风之灵效果
	def Qfzl(self,champion):
		champion.enemy.champion.defensive_attribute.Add_tenacity(champion.enemy.flag.weapon_flag.qfzl[1])
		champion.enemy.flag.weapon_flag.qfzl[2] = True
		champion.enemy.flag.weapon_flag.qfzl[3] += 1
	# 基克先驱效果
	def Jkxq(self,champion):
		numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
		num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
		if not champion.flag.special_flag.dead_area[0]:
			for i in range(3):
				if numTF[i] and (not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag)\
				and (not champion.game.LR[champion.position][num_pos[i]].flag.special_flag.dead_area[0]) and not champion.flag.weapon_flag.jkxq[2][i]:
					if champion.game.LR[champion.position][num_pos[i]].champion.name == 'Jhin':
						champion.game.LR[champion.position][num_pos[i]].As2cr(1 + champion.flag.weapon_flag.jkxq[1])
					else:
						champion.game.LR[champion.position][num_pos[i]].champion.attack_attribute.attack_speed *= (1 + champion.flag.weapon_flag.jkxq[1])
					champion.flag.weapon_flag.jkxq[2][i] = True
					champion.game.LR[champion.position][num_pos[i]].flag.special_flag.halo['基克先驱'] = True
		else:
			for i in range(3):
				if numTF[i]:
					if champion.game.LR[champion.position][num_pos[i]] == champion and not champion.flag.weapon_flag.jkxq[2][i]:
						champion.game.LR[champion.position][num_pos[i]].champion.attack_attribute.attack_speed *= (1 + champion.flag.weapon_flag.jkxq[1])
						champion.flag.weapon_flag.jkxq[2][i] = True
						champion.game.LR[champion.position][num_pos[i]].flag.special_flag.halo['基克先驱'] = True
	# 冰霜之心效果
	def Bszx(self,champion):
		numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
		num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
		if not champion.flag.special_flag.dead_area[0]:
			for i in range(3):
				if numTF[i] and not (champion.game.LR[~champion.position+2][num_pos[i]].flag.condition_flag.death_flag)\
				and (not champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.dead_area[0]) and not champion.flag.weapon_flag.bszx[2][i]\
				and not champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.Nabasre_flag:
					if champion.game.LR[~champion.position+2][num_pos[i]].champion.name == 'Jhin':
						champion.game.LR[~champion.position+2][num_pos[i]].As2cr(1 - champion.flag.weapon_flag.bszx[1])
					else:
						champion.game.LR[~champion.position+2][num_pos[i]].champion.attack_attribute.attack_speed *= (1 - champion.flag.weapon_flag.bszx[1])
					champion.flag.weapon_flag.bszx[2][i] = True
					champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.halo['冰霜之心'] = True 
		else:
			for i in range(3):
				if numTF[i]:
					if champion.game.LR[~champion.position+2][num_pos[i]] == champion.flag.special_flag.dead_area[1] and not champion.flag.weapon_flag.bszx[2][i]\
					and not champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.Nabasre_flag:
						champion.game.LR[~champion.position+2][num_pos[i]].champion.attack_attribute.attack_speed *= (1 - champion.flag.weapon_flag.bszx[1])
						champion.flag.weapon_flag.bszx[2][i] = True
						champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.halo['冰霜之心'] = True
	# 深渊面具效果
	def Symj(self,champion):
		numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
		num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
		if not champion.flag.special_flag.dead_area[0]:
			for i in range(3):
				if numTF[i] and not (champion.game.LR[~champion.position+2][num_pos[i]].flag.condition_flag.death_flag)\
				and (not champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.dead_area[0]) and not champion.flag.weapon_flag.symj[4][i]:
					champion.game.LR[~champion.position+2][num_pos[i]].flag.weapon_flag.symj[1] = True
					champion.flag.weapon_flag.symj[4][i] = True
					champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.halo['深渊面具'] = True
		else:
			for i in range(3):
				if numTF[i]:
					if champion.game.LR[~champion.position+2][num_pos[i]] == champion.flag.special_flag.dead_area[1] and not champion.flag.weapon_flag.symj[4][i]:
						champion.game.LR[~champion.position+2][num_pos[i]].flag.weapon_flag.symj[1] = True
						champion.flag.weapon_flag.symj[4][i] = True
						champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.halo['深渊面具'] = True
	# 泰坦坚决效果
	def Ttjj(self,champion):
		champion.flag.weapon_flag.ttjj[1][0] += 1
		if not champion.flag.weapon_flag.ttjj[3]:
			champion.flag.weapon_flag.ttjj[2][0] += champion.flag.weapon_flag.ttjj[2][1]
		else:
			champion.flag.weapon_flag.ttjj[2][0] += (2 * champion.flag.weapon_flag.ttjj[2][1])
		if champion.flag.weapon_flag.ttjj[1][0] >= champion.flag.weapon_flag.ttjj[1][1] and not champion.flag.weapon_flag.ttjj[3]:
			champion.flag.weapon_flag.ttjj[3] = True
			champion.champion.defensive_attribute.armor += champion.flag.weapon_flag.ttjj[2][2]
			champion.champion.defensive_attribute.spell_resistance += champion.flag.weapon_flag.ttjj[2][3]
	# 斑比熔渣效果
	def Bbrz(self,champion):
		numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
		num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
		end_flag = champion.flag.weapon_flag.bbrz[1][0].Duration(champion.flag.weapon_flag.bbrz[1][1])
		if end_flag:
			if champion.flag.special_flag.dead_area[0] :
				if champion.flag.special_flag.dead_area[1] == champion.game.LR[~champion.position+2][champion.pos_num] \
				and not champion.flag.special_flag.dead_area[1].flag.condition_flag.miss_flag[0]:
					self.Bbrz_deal(champion,champion.flag.special_flag.dead_area[1])
			else:
				for i in range(3):	
					if numTF[i]:
						if not champion.game.LR[~champion.position+2][num_pos[i]].flag.condition_flag.death_flag \
						and not champion.game.LR[~champion.position+2][num_pos[i]].flag.condition_flag.miss_flag[0] \
						and not champion.game.LR[~champion.position+2][num_pos[i]].flag.special_flag.dead_area[0]:
							self.Bbrz_deal(champion,champion.game.LR[~champion.position+2][num_pos[i]])
	# 斑比熔渣伤害计算
	def Bbrz_deal(self,champion,enemy):
		# 不受法强加成
		if enemy.flag.condition_flag.buff_invincible_flag:
			pass
		else:
			if enemy.flag.weapon_flag.symj[1]: 											# 触发深渊面具效果
				enemy.flag.weapon_flag.symj[2] = 1 + enemy.flag.weapon_flag.symj[3]
			bbrz_damage = (champion.flag.weapon_flag.bbrz[2] * (100 / (100 + (enemy.champion.defensive_attribute.spell_resistance \
				* ((1 - champion.champion.attack_attribute.spell_resistance_penetration/100)))))) * enemy.flag.weapon_flag.symj[2] * enemy.condition.matigation.value * enemy.condition.iron.value
			if enemy.flag.weapon_flag.jlzy[0]: 											# 触发敌人的巨龙之牙效果
				bbrz_damage *= (1 - enemy.flag.weapon_flag.jlzy[1])
			# 扣血、击杀判断、累计造成伤害
			champion.enemy.champion.hp.HP_reduce(bbrz_damage,champion,enemy)
			champion.champion.attack_attribute.all_damage.spell_damage += bbrz_damage
			champion.champion.attack_attribute.all_damage.Total_damage_calculation()		
	# 巨石板甲效果
	def Jsbj(self,champion):
		champion.flag.weapon_flag.jsbj[1] += 1
		if champion.flag.weapon_flag.jsbj[1] >= 3:
			champion.champion.defensive_attribute.armor += champion.flag.weapon_flag.jsbj[2][0]
			champion.champion.defensive_attribute.spell_resistance += champion.flag.weapon_flag.jsbj[2][1]
			champion.champion.defensive_attribute.dodge_mechanism.Add_dodge(champion.flag.weapon_flag.jsbj[2][2])
			champion.champion.defensive_attribute.Add_tenacity(champion.flag.weapon_flag.jsbj[2][3])
			champion.flag.weapon_flag.jsbj[3] += 1
			champion.flag.weapon_flag.jsbj[4] = True
			champion.flag.weapon_flag.jsbj[1] = 0
	# 神臂之弓效果
	def Sbzg(self,champion,mode):   # mode = 0表示普攻攻击特效触发，=1表示技能附带攻击特效触发
		if champion.enemy.flag.condition_flag.debuff_burn_flag or champion.enemy.flag.condition_flag.debuff_dizz_flag \
		or champion.enemy.flag.condition_flag.debuff_frozen_flag or champion.enemy.flag.condition_flag.debuff_silence_flag \
		or champion.enemy.flag.condition_flag.debuff_disarm_flag or champion.enemy.flag.condition_flag.debuff_injury_flag:
			if mode == 0:
				champion.champion.attack_attribute.normal_attack_damage.physical_damage *= (1 + champion.flag.weapon_flag.sbzg[1])
				champion.champion.attack_attribute.normal_attack_damage.spell_damage *= (1 + champion.flag.weapon_flag.sbzg[1])
				champion.champion.attack_attribute.normal_attack_damage.real_damage *= (1 + champion.flag.weapon_flag.sbzg[1])
			else:
				champion.champion.attack_attribute.spell_attack_damage.physical_damage *= (1 + champion.flag.weapon_flag.sbzg[1])
				champion.champion.attack_attribute.spell_attack_damage.spell_damage *= (1 + champion.flag.weapon_flag.sbzg[1])
				champion.champion.attack_attribute.spell_attack_damage.real_damage *= (1 + champion.flag.weapon_flag.sbzg[1])
			champion.flag.weapon_flag.sbzg[2] = True
			champion.flag.weapon_flag.sbzg[3] += 1
	# 雷霆劫掠效果
	def Ltjl(self,champion):
		# 震击伤害
		thud_damage = champion.flag.weapon_flag.ltjl[1] * champion.champion.attack_attribute.spell_power * champion.enemy.condition.iron.value
		# 计算扣血、判断击杀
		if not champion.enemy.flag.condition_flag.buff_invincible_flag:
			champion.enemy.champion.hp.HP_reduce(thud_damage,champion,champion.enemy)
			if not champion.enemy.flag.condition_flag.buff_invincible_flag:
				# 感电效果
				champion.enemy.condition.electrification.Add_electrification(champion.enemy, champion.flag.weapon_flag.ltjl[2])
			# 累计造成伤害(敌人)
			champion.champion.attack_attribute.all_damage.real_damage += thud_damage
			champion.champion.attack_attribute.all_damage.Total_damage_calculation()
			# 触发雷霆羁绊
			if champion.flag.rela_flag['雷霆'][0] and thud_damage > 0:
				champion.champion.relatedness.Thunder(champion)
			# 显示效果、计数
			champion.flag.weapon_flag.ltjl[3] = True
			champion.flag.weapon_flag.ltjl[4] += 1
	# 荣光凯旋效果
	def Rgkx(self,champion):
		# 回复生命值(不受法强加成)
		value_treatment = champion.flag.weapon_flag.rgkx[2] * (champion.champion.hp.max_value - champion.champion.hp.value)
		champion.champion.hp.HP_restore(value_treatment, champion.champion, champion)
		champion.flag.weapon_flag.rgkx[3] = True
		champion.flag.weapon_flag.rgkx[4] += 1
	# 暗影核心效果
	def Ayhx(self,champion):
		if champion.flag.weapon_flag.ayhx[1][0]:
			end_flag = champion.flag.weapon_flag.ayhx[1][1].Duration(champion.flag.weapon_flag.ayhx[1][2])
			if end_flag:
				champion.flag.weapon_flag.ayhx[1][0] = False
	# 爆破炸弹效果
	def Bpzd(self,champion,enemy):
		# 不受法强加成
		if enemy.flag.weapon_flag.symj[1]: 											# 触发深渊面具效果
			enemy.flag.weapon_flag.symj[2] = 1 + enemy.flag.weapon_flag.symj[3]
		bpzd_damage = (champion.flag.weapon_flag.bpzd[1] * (100 / (100 + (enemy.champion.defensive_attribute.spell_resistance \
			* ((1 - champion.champion.attack_attribute.spell_resistance_penetration/100)))))) * enemy.flag.weapon_flag.symj[2] * enemy.condition.matigation.value
		if enemy.flag.weapon_flag.jlzy[0]: 											# 触发敌人的巨龙之牙效果
			bpzd_damage *= (1 - enemy.flag.weapon_flag.jlzy[1])
		# 卡萨丁贤者之石被动
		if enemy.champion.name == 'Kassadin':
			champion.champion.attack_attribute.spell_attack_damage.spell_damage *= (1 - enemy.champion.skill.para[3])
		# 扣血、击杀判断、累计造成伤害
		champion.enemy.champion.hp.HP_reduce(bpzd_damage,champion,enemy)
		champion.champion.attack_attribute.all_damage.spell_damage += bpzd_damage
		champion.champion.attack_attribute.all_damage.Total_damage_calculation()
		# 显示
		champion.flag.weapon_flag.bpzd[2] = True
		# 触发次数计数
		champion.flag.weapon_flag.bpzd[3] += 1
	# 虚空之门效果：召唤虚空兽
	def Xkzm(self,champion):
		# 死亡处理
		champion.Death_deal()
		VoidMonster[champion.position][champion.pos_num].__init__()
		VoidMonster[champion.position][champion.pos_num].position = champion.position
		VoidMonster[champion.position][champion.pos_num].pos_num = champion.pos_num
		VoidMonster[champion.position][champion.pos_num].game = champion.game
		VoidMonster[champion.position][champion.pos_num].enemy = champion.enemy
		VoidMonster[champion.position][champion.pos_num].champion.relatedness.element[1] = 2
		VoidMonster[champion.position][champion.pos_num].champion.relatedness.profession[1] = 2
		champion.game.LR[champion.position][champion.pos_num] = VoidMonster[champion.position][champion.pos_num]
		for i in range(3):
			VoidMonster[champion.position][champion.pos_num].friend[i] = champion.game.LR[champion.position][i]
		champion.game.LR_ui[champion.position][champion.pos_num] = Champion_Interface(champion.game.screen,VoidMonster[champion.position][champion.pos_num],champion.game)
		VM = VoidMonster[champion.position][champion.pos_num]
		# 虚空入侵效果
		VM.champion.attack_attribute.AD += VM.champion.skill.para[0] * (champion.champion.defensive_attribute.armor + champion.champion.defensive_attribute.spell_resistance)
		# 嘲讽
		numTF = [True, VM.pos_num - 1 >= 0, VM.pos_num + 1 <= 2]
		num_pos = [VM.pos_num, VM.pos_num - 1, VM.pos_num + 1]
		for i in range(3):
			if numTF[i]:
				if not VM.game.LR[~VM.position+2][num_pos[i]].flag.condition_flag.death_flag and not VM.game.LR[~VM.position+2][num_pos[i]].flag.condition_flag.miss_flag[0] \
				and not VM.game.LR[~VM.position+2][num_pos[i]].flag.condition_flag.buff_invincible_flag and not VM.game.LR[~VM.position+2][num_pos[i]].flag.condition_flag.buff_unstoppable_flag:
					VM.game.LR[~VM.position+2][num_pos[i]].enemy = VM
		print('警报：虚空入侵！')
	# 夜之锋刃效果
	def Yzfr(self,champion):
		if not champion.flag.weapon_flag.yzfr[2]:
			if champion.flag.weapon_flag.yzfr[3][0].Duration(champion.flag.weapon_flag.yzfr[3][1]):
				champion.flag.weapon_flag.yzfr[2] = True
				champion.condition.magic_shield.Add_magic_shield(champion,100)
	# 魅惑挂坠效果
	def Mhgz(self,champion):
		numTF = [True, champion.pos_num - 1 >= 0, champion.pos_num + 1 <= 2]
		num_pos = [champion.pos_num, champion.pos_num - 1, champion.pos_num + 1]
		for i in range(3):
			if numTF[i] and not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.death_flag \
			 and not champion.game.LR[champion.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
			 	champion.game.LR[champion.position][num_pos[i]].champion.mp.Calculation(champion.game.LR[champion.position][num_pos[i]],champion.flag.weapon_flag.mhgz[1])
			 	champion.flag.weapon_flag.mhgz[2] = True
			 	champion.flag.weapon_flag.mhgz[3] += 1
	# 巨型九头蛇效果
	def Jxjts(self,champion):
		enemy = champion.enemy
		num_pos = [champion.enemy.pos_num - 1, champion.enemy.pos_num + 1]
		numTF = [(num_pos[0] >= 0 and not champion.game.LR[~champion.position+2][num_pos[0]].flag.condition_flag.death_flag and not champion.game.LR[~champion.position+2][num_pos[0]].flag.condition_flag.miss_flag[0]), \
		(num_pos[1] <= 2 and not champion.game.LR[~champion.position+2][num_pos[1]].flag.condition_flag.death_flag and not champion.game.LR[~champion.position+2][num_pos[1]].flag.condition_flag.miss_flag[0])]
		# 顺劈溅射伤害标志
		champion.flag.weapon_flag.jxjts[2] = True
		# 伤害计算
		for i in range(2):
			if numTF[i]:
				# 判断目标
				champion.enemy = champion.game.LR[~champion.position+2][num_pos[i]]
				dodge_flag = False # 溅射伤害不会被闪避
				# 复制普攻伤害原值
				champion.champion.attack_attribute.normal_attack.physical_damage = champion.champion.attack_attribute.normal_attack_orig.physical_damage
				champion.champion.attack_attribute.normal_attack.spell_damage = champion.champion.attack_attribute.normal_attack_orig.spell_damage
				champion.champion.attack_attribute.normal_attack.real_damage = champion.champion.attack_attribute.normal_attack_orig.real_damage
				champion.Normal_attack_damage_calculation()
				# 计算敌人回蓝
				champion.champion.mp.MP_restore_2(champion.flag, champion, champion.enemy, 1)
		champion.flag.weapon_flag.jxjts[2] = False
		champion.enemy = enemy

# 武器、羁绊
if True:
	# 基础武器字典
	basic_weapon = {1 : '暴风大剑', 2 : '反曲之弓', 3 : '女神之泪', 4 : '巨人腰带', 5 : '钢铁锁甲',\
	 6 : '负极斗篷', 7 : '无用大棒', 8 : '格斗手套', 9 : '金色魔铲'}
	bwd = [None for _ in range(9)]
	bwd[0] = ['暴风大剑：+10点AD','暴风大剑：+20点AD','暴风大剑：+30点AD']
	bwd[1] = ['反曲之弓：+15%攻速','反曲之弓：+22.5%攻速','反曲之弓：+33.75%攻速']
	bwd[2] = ['女神之泪：+20点法力值','女神之泪：+40点法力值','女神之泪：+60点法力值']
	bwd[3] = ['巨人腰带：+200点最大生命值','巨人腰带：+400点最大生命值','巨人腰带：+600点最大生命值']
	bwd[4] = ['钢铁锁甲：+25点护甲','钢铁锁甲：+50点护甲','钢铁锁甲：+75点护甲']
	bwd[5] = ['负极斗篷：+20点魔抗、+10%韧性','负极斗篷：+40点魔抗、+20%韧性','负极斗篷：+60点魔抗、+30%韧性']
	bwd[6] = ['无用大棒：+20%法强','无用大棒：+40%法强','无用大棒：+60%法强']
	bwd[7] = ['格斗手套：+10%暴击率','格斗手套：+20%暴击率','格斗手套：+30%暴击率']
	if version[0] == 2:
		bwd[8] = ['金色魔铲：+5%闪避率']
	elif version[0] in (1,3):
		bwd[8] = ['金色魔铲：+10%闪避率','金色魔铲：+20%闪避率','金色魔铲：+30%闪避率']
	basic_weapon_describe = {'暴风大剑' : bwd[0], '反曲之弓' : bwd[1], '女神之泪' : bwd[2], '巨人腰带' : bwd[3], '钢铁锁甲' : bwd[4], \
	'负极斗篷' : bwd[5], '无用大棒' : bwd[6], '格斗手套' : bwd[7], '金色魔铲' : bwd[8]}

	# 进阶武器字典
	#	效果描述
	wd = [None for _ in range(73)]
	wd[0] = ['领主之刃：获得额外的10点AD，之后','每击杀(普攻击杀)一个敌人会再获得','15点AD','层数：0']
	wd[1] = ['巨人杀手：普攻会额外造成相当于目','标2%(最大生命值+护盾值)的真实伤害']
	wd[2] = ['朔极之矛：第一次施法后，每次普攻','额外回复自身12%最大法力值']
	wd[3] = ['基克先驱：自己及周围的队友增加15%','攻速']
	wd[4] = ['守护天使：濒临死亡时触发，进入2s','的不可选取状态，清除自身除重伤以','外的状态，然后恢复400点生命值复','活，仅触发一次']
	wd[5] = ['饮血巨剑：获得55%生命偷取并可以过','量治疗，将额外治疗量转化为护盾，','持续10s']
	wd[6] = ['科技枪刃：35%全伤害吸血']
	wd[7] = ['无尽之刃：增加额外10%暴击率和100%','暴击伤害']
	wd[8] = ['疾射火炮：额外获得10%攻速和10%暴','击率，且普攻不会被闪避(>幻影之舞)']
	wd[9] = ['狂热电刀：每进行3次普攻，便会对敌','方一连线的英雄造成50点魔法伤害','触发次数：0']
	wd[10] = ['卑劣手斧：普攻会给自己增加(造成普','攻物理伤害/2.0)的护盾，持续1.5s','累计护盾值：0']
	wd[11] = ['幻影之舞：闪避所有暴击，并且不会','被穿甲、削甲','闪避暴击次数：0']
	wd[12] = ['分裂飓风：普攻时会对附近的一个敌','人进行额外的一次普攻，造成35%的伤','害并附带攻击特效','额外目标：无']
	wd[13] = ['鬼索之怒：每次普攻增加4%攻速','层数：0']
	wd[14] = ['凡性提醒：获得45点穿甲，并且普攻','会对敌人造成重伤效果，持续3s']
	wd[15] = ['天使之拥：技能施放后立即恢复30点','法力值']
	wd[16] = ['神圣救赎：生命值低于30%最大生命值','时触发，2.5s后治疗自己及周围队友','300点生命值']
	wd[17] = ['冰霜之心：降低周围敌人15%攻速']
	wd[18] = ['沉默匕首：普攻有33%几率使敌人沉默','(不能获得法力值，并且能打断持续施','法技能)，持续2.5s','触发次数：0']
	wd[19] = ['卢登回声：伤害型技能命中中心目标','时对目标周围的敌人造成90点魔法伤','害溅射，每次施法只能触发一次']
	wd[20] = ['正义之手：每次普攻增加30%物理造成','伤害或者回复30点生命值','触发增伤次数：0','触发回血次数：0']
	wd[21] = ['狂徒铠甲：每秒回复2.5%已损生命值，','上限为每秒回复40点生命值']
	wd[22] = ['泰坦坚决：受到伤害或打出暴击时叠','加一层2%的伤害加成；25层时获得180','点护甲、魔抗，且后续伤害加成翻倍','层数：0']
	wd[23] = ['深渊面具：附近敌人额外承受25%魔法','伤害']
	wd[24] = ['死亡秘典：获得35点法穿且技能造成','伤害时给敌人造成重伤效果，持续8s']
	wd[25] = ['伏击之爪：无视受到的的第一次(中','心)技能，并使敌人眩晕4s']
	wd[26] = ['荆棘之甲：收到普攻伤害时以真实伤','害形式反弹85%缓和伤害，并给敌人','造成重伤效果，持续3s']
	wd[27] = ['折戟秘刀：普攻有30%几率使敌人缴械','(不能进行普攻)，持续2.5s','触发次数：0']
	wd[28] = ['烈阳之匣：为自己和周围队友提供250','点护盾，持续6s']
	wd[29] = ['冰脉护手：额外增加10%闪避率，每次','触发闪避时降低攻击者及其周围英雄','5%攻速','触发次数：0']
	wd[30] = ['巨龙之牙：额外减免50%魔法伤害']
	wd[31] = ['离子火花：敌人施放技能时给敌人造成','同等敌人最大法力值(上限90)的真实','伤害','触发次数：0']
	wd[32] = ['水银披风：携带者处于不可阻挡状态，','持续30s']
	wd[33] = ['灭世之帽：法强额外增幅50%']
	wd[34] = ['珠光拳套：获得额外5%暴击率，技能','也可造成暴击','触发次数：0']
	wd[35] = ['窃贼手套：随机额外偷到3个基本武器','待定','待定','待定']
	wd[36] = ['夜袭暮刃：携带者同时也是刺客；','获得额外20点穿甲；在施法后的第一','下普攻触发暴击并附带30点额外物理','伤害']
	wd[37] = ['神臂之弓：携带者同时也是游侠；','额外获得8%攻速并且普攻对异常状态','的敌人多造成40%伤害','触发次数：0']
	wd[38] = ['巫师法帽：携带者同时也是法师；','濒死时令生命值=10，并处于不可选取','状态2.5s']
	wd[39] = ['极地战锤：携带者同时也是极地元素；','造成的冰冻、眩晕效果+1s','触发次数：0']
	wd[40] = ['巨石板甲：携带者同时也是守护神；','每受到3次攻击，增加6点护甲、5点魔','抗、2%闪避率、2%韧性','层数：0']
	wd[41] = ['炽热香炉：携带者同时也是秘术师；','技能的护盾及治疗效果可令目标单位','处于炽热状态：提升25%攻速、获得','25%生命偷取，持续5s']
	wd[42] = ['斑比熔渣：携带者同时也是地狱火；','每秒对每个周围的敌人造成5点魔法','伤害']
	wd[43] = ['黑暗切割：携带者同时也是狂战士；','普攻会减少敌人8%的护甲，最多叠加','6次']
	wd[44] = ['飞升护符：携带者同时也是光元素；','触发闪避时增加4%攻速','触发次数：0']
	# S2武器
	wd[45] = ['清风之灵：携带者同时也是云霄元素；','触发闪避时增加15%韧性','触发次数：0']
	wd[46] = ['雷霆劫掠：携带者同时也是雷霆元素；','造成暴击时对目标震击造成30点真实','伤害并使其感电2s','触发震击次数：0']
	wd[47] = ['破败王者：携带者同时也是剑士；','普攻会造成目标3%当前生命值(包括护','盾值)的额外物理伤害']
	wd[48] = ['暗影核心：携带者同时也是影元素；','6s内伤害增幅65%，击杀后刷新']
	wd[49] = ['樱手里剑：携带者同时也是忍者；','获得20点能量且在击杀目标后可回复','自身35%最大能量','触发次数：0']
	# 奥恩升级的12种武器
	wd[50] = ['熔火之刃：增加额外15%暴击率和110%','暴击伤害']
	wd[51] = ['灭世之冠：法强额外增幅70%']
	wd[52] = ['卢登脉冲：伤害型技能命中中心目标','时对目标周围的敌人造成110点魔法伤','害溅射，每次施法只能触发一次']
	wd[53] = ['烈阳之环：为自己和周围队友提供280','点护盾，持续8s']
	wd[54] = ['邪龙之牙：额外减免65%魔法伤害']
	wd[55] = ['荆棘之咬：收到普攻伤害时以真实伤','害形式反弹100%缓和伤害，并给敌人','造成重伤效果，持续3s']
	wd[56] = ['炼狱面具：附近敌人额外承受30%魔法','伤害']
	wd[57] = ['冰封之心：降低周围敌人20%攻速']
	wd[58] = ['基克聚合：自己及周围的队友增加20%','攻速']
	wd[59] = ['神圣拯救：生命值低于30%最大生命值','时触发，1.5s后治疗自己及周围队友','333点生命值']
	wd[60] = ['附魔枪刃：40%全伤害吸血']
	wd[61] = ['天使之吻：技能施放后立即恢复40点','法力值']
	# S2后续改动武器
	wd[62] = ['荣光凯旋：额外获得50点最大生命值，','击杀敌人后立刻恢复20%已损生命值','触发次数：0']
	# S3武器
	wd[63] = ['爆破炸弹：携带者同时也是爆破专家；','造成眩晕效果时追加50点魔法伤害','触发次数：0']
	wd[64] = ['淬炼勋章：携带者同时也是奥德赛；','施放技能后获得一个持续4s的护盾，','护盾值为10%的最大生命值，5s内不可','重复触发']
	wd[65] = ['魅惑挂坠：携带者同时也是星之守护','者；每次施放技能时，为周围的友军','提供15点法力值','触发次数：0']
	wd[66] = ['夜之锋刃：携带者同时也是刺客；','获得额外15点穿甲并且每隔12s获得一','个魔法护盾','格挡技能次数：0']
	wd[67] = ['星神法球：携带者同时也是星神；','获得的治疗效果提升15%']
	wd[68] = ['黑暗之心：携带者同时也是暗星；','单次造成伤害超过150时，使目标重伤','5s','触发次数：0']
	wd[69] = ['圣银胸甲：携带者同时也是护卫；','生命值低于40%时，护甲和魔抗提升','40%']
	wd[70] = ['虚空之门：携带者死后会打开虚空之','门召唤虚空兽，虚空兽造成真实伤害','并且会嘲讽周围的敌人']
	wd[71] = ['静止法衣：向对位的敌人射出一道光','线，令其处于破法状态']
	wd[72] = ['巨型九头蛇：盖伦专属武器，普攻会','顺劈面前区域，对目标周围的敌人造','成70%的溅射伤害']

	advance_weapon = {'领主之刃' : wd[0], '巨人杀手' : wd[1], '朔极之矛' : wd[2], '基克先驱' : wd[3], '守护天使' : wd[4], '饮血巨剑' : wd[5], '科技枪刃' : wd[6], '无尽之刃' : wd[7], \
	'疾射火炮' : wd[8], '狂热电刀' : wd[9], '卑劣手斧' : wd[10], '幻影之舞' : wd[11], '分裂飓风' : wd[12], '鬼索之怒' : wd[13], '凡性提醒' : wd[14], '天使之拥' : wd[15], \
	'神圣救赎' : wd[16], '冰霜之心' : wd[17], '沉默匕首' : wd[18], '卢登回声' : wd[19], '正义之手' : wd[20], '狂徒铠甲' : wd[21], '泰坦坚决' : wd[22], '深渊面具' : wd[23], \
	'死亡秘典' : wd[24], '伏击之爪' : wd[25], '荆棘之甲' : wd[26], '折戟秘刀' : wd[27], '烈阳之匣' : wd[28], '冰脉护手' : wd[29], '巨龙之牙' : wd[30], '离子火花' : wd[31], \
	'水银披风' : wd[32], '灭世之帽' : wd[33], '珠光拳套' : wd[34], '窃贼手套' : wd[35], '夜袭暮刃' : wd[36], '神臂之弓' : wd[37], '巫师法帽' : wd[38], '极地战锤' : wd[39], \
	'巨石板甲' : wd[40], '炽热香炉' : wd[41], '斑比熔渣' : wd[42], '黑暗切割' : wd[43], '飞升护符' : wd[44], '清风之灵' : wd[45], '雷霆劫掠' : wd[46], '破败王者' : wd[47], \
	'暗影核心' : wd[48], '樱手里剑' : wd[49], '熔火之刃' : wd[50], '灭世之冠' : wd[51], '卢登脉冲' : wd[52], '烈阳之环' : wd[53], '邪龙之牙' : wd[54], '荆棘之咬' : wd[55], \
	'炼狱面具' : wd[56], '冰封之心' : wd[57], '基克聚合' : wd[58], '神圣拯救' : wd[59], '附魔枪刃' : wd[60], '天使之吻' : wd[61], '荣光凯旋' : wd[62], '爆破炸弹' : wd[63], \
	'淬炼勋章' : wd[64], '魅惑挂坠' : wd[65], '夜之锋刃' : wd[66], '星神法球' : wd[67], '黑暗之心' : wd[68], '圣银胸甲' : wd[69], '虚空之门' : wd[70], '静止法衣' : wd[71], \
	'巨型九头蛇' : wd[72]}

	# 羁绊数量
	r_num = [43]
	# 羁绊字典
	r_dic = {1 : '光', 2 : '极地', 3 : '森林', 4 : '水晶', 5 : '海洋', 6: '钢铁', 7 : '地狱火', 8 : '影', 9 : '沙漠', 10 : '游侠', \
	11 : '掠食者', 12 : '秘术师', 13 : '守护神', 14 : '法师', 15: '刺客', 16 : '狂战士', 17 : '大元素使', 18 : '黯焰', 19 : '恕瑞玛之皇', \
	20 : '太阳圆盘', 21 : '斗士', 22 : '银月', 23 : '剧毒', 24 : '剑士', 25 : '枪手', 26 : '云霄', 27 : '雷霆', 28 : '忍者', 29 : '忍剑士', \
	30 : '银河机神', 31 : '奥德赛', 32 : '未来战士', 33 : '星神', 34 : '星之守护者', 35 : '暗星', 36 : '爆破专家', 37 : '源计划', \
	38 : '护卫', 39 : '星舰龙神', 40 : '虚空', 41 : '先锋', 42 : '银河魔装机神', 43 : '异星人'}

	# 	羁绊效果
	rd = [[None for _ in range(2)] for _ in range(r_num[0])]
	rd[0][0] = ['光：死亡时治疗队友并提升其攻速','(2)：治疗25%最大生命值、+30%攻速','(3)：治疗35%最大生命值、+40%攻速','(4)：治疗45%最大生命值、+50%攻速']
	rd[0][1] = [[0.25,0.3],[0.35,0.4],[0.45,0.5]]
	rd[1][0] = ['极地：普攻有几率冰冻目标1.5s','(2)：25%几率','(3)：45%几率','(4)：65%几率']
	rd[1][1] = [0.25,0.45,0.65,1.5]
	rd[2][0] = ['森林：每2s秒回复生命值','(2)：回复20点生命值','(3)：回复30点生命值','(4)：回复40点生命值']
	rd[2][1] = [20,30,40,2]
	rd[3][0] = ['水晶：单次承受伤害上限','(2)：上限60点','(3)：上限40点','(4)：上限20点']
	rd[3][1] = [60,40,20]
	rd[4][0] = ['海洋：每4s回复全队法力值','(2)：回复20点法力值','(3)：回复40点法力值','(4)：回复60点法力值']
	rd[4][1] = [20,40,60,4]
	rd[5][0] = ['钢铁：<50%生命进入钢铁状态(免伤)','(2)：持续5s','(3)：持续10s','(4)：持续15s']
	rd[5][1] = [5,10,15,0.5]
	rd[6][0] = ['沙漠：(开场时)削减敌方全队的护甲','(2)：削减40%护甲','(3)：削减70%护甲','(4)：削减100%护甲']
	rd[6][1] = [0.4,0.7,1.0]
	rd[7][0] = ['游侠：每过几s后攻速翻倍，持续3s','(2)：每过5s','(3)：每过2.5s']
	rd[7][1] = [5,2.5,3]
	rd[8][0] = ['掠食者：全伤害斩杀低血线的目标','(2)：生命值低于20%','(3)：生命值低于25%']
	rd[8][1] = [0.2,0.25]
	rd[9][0] = ['秘术师：为全队增加魔抗','(2)：+70魔抗','(3)：+140魔抗']
	rd[9][1] = [70,140]
	rd[10][0] = ['守护神：提升护甲','(2)：+80护甲','(3)：+160护甲']
	rd[10][1] = [80,160]
	rd[11][0] = ['法师：提升法强','(固有：双倍基础回蓝)','(2)：+50%法强','(3)：+100%法强']
	rd[11][1] = [0.5,1]
	rd[12][0] = ['刺客：增加暴击率和暴击伤害','(固有：+15穿甲、+15法穿)','(2)：+20%暴击率、+50%暴击伤害','(3)：+40%暴击率、+100%暴击伤害']
	rd[12][1] = [[0.2,0.5],[0.4,1]]
	rd[13][0] = ['狂战士：普攻有几率会顺劈，对周围','敌人造成70%溅射伤害并附带攻击特效','(2)：50%几率','(3)：100%几率，获得额外15AD']
	rd[13][1] = [0.5,1.0,0.7,15]
	if version[0] == 1:
		rd[14][0] = ['大元素使：大元素使会随机获得一种','元素(不含沙漠元素)，并且元素羁绊','按双倍计算']
	elif version[0] == 2:
		rd[14][0] = ['大元素使：大元素使会随机获得一种','元素(不含剧毒、银月元素)，并且元','素羁绊按双倍计算']
	rd[15][0] = ['地狱火：普攻有33%几率使敌人灼烧3s','(2)：每秒灼烧3%最大生命真实伤害','(3)：每秒灼烧5%最大生命真实伤害','(4)：每秒灼烧7%最大生命真实伤害']
	rd[15][1] = [0.03,0.05,0.07,3,0.33,0.015]
	rd[16][0] = ['影：普攻、技能一部分转为真实伤害','(2)：40%转化','(3)：70%转化','(4)：100%转化']
	rd[16][1] = [0.4,0.7,1]
	rd[17][0] = ['黯焰：黯焰元素同时是地狱火元素和','影元素']
	rd[18][0] = ['恕瑞玛之皇：自身的沙漠元素羁绊按','双倍计算；当有未死亡的沙漠元素友','军(包括太阳圆盘)时，获得50%的减伤','状态']
	rd[18][1] = [0.5]
	rd[19][0] = ['太阳圆盘：太阳圆盘免疫控制效果，','每秒减少50点生命值；太阳圆盘的沙','漠元素不参与羁绊计算']
	rd[20][0] = ['斗士：获得额外生命值','(2)：获得额外300点生命值','(3)：获得额外600点生命值']
	rd[20][1] = [300,600]
	rd[21][0] = ['银月：每过7s，全队获得暴击率、暴','击伤害和法强加成(至多可叠加4层)','(2)：15%、15%、10%','(3)：25%、25%、20%']
	rd[21][1] = [[0.15,0.15,0.1],[0.25,0.25,0.2],7,4]
	rd[22][0] = ['剧毒：技能造成伤害时会令目标中毒：','减少法力值的回复(持续5s)','(2)：减少50%法力回复','(3)：减少80%法力回复']
	rd[22][1] = [0.5,0.8,5]
	rd[23][0] = ['剑士：普攻后有45%几率攻速乘以3，','持续数次普攻后恢复(不可叠加)','(2)：2次普攻后恢复','(3)：4次普攻后恢复']
	rd[23][1] = [2,4,0.45,3]
	rd[24][0] = ['枪手：普攻后一定几率打出额外攻击，','额外攻击附带攻击特效','(2)：80%几率对1个敌人打出额外攻击','(3)：90%几率对2个敌人打出额外攻击']
	rd[24][1] = [[0.8,1],[0.9,2],1.0]
	rd[25][0] = ['云霄：全队增加闪避率','(2)：增加15%闪避率','(3)：增加30%闪避率','(4)：增加45%闪避率']
	rd[25][1] = [0.15,0.3,0.45]
	rd[26][0] = ['雷霆：造成伤害几率落雷命中随机敌人','(2)：40%几率，造成30魔法伤害','(3)：45%几率，造成35魔法伤害','(4)：50%几率，造成40魔法伤害']
	rd[26][1] = [[0.40,30],[0.45,35],[0.50,40]]
	rd[27][0] = ['忍者：若干个忍者提升60%伤害','(固有：忍者使用能量机制)','(2)：随机一个忍者伤害提升','(3)：所有忍者伤害提升']
	rd[27][1] = [1,3,0.6]
	rd[28][0] = ['忍剑士：忍剑士同时是忍者和剑士']
	rd[29][0] = ['银河机神：开局会合体召唤银河魔装','机神，直到机神倒下后再解体','(2)：合体召唤机神盖伦','(3)：合体召唤机神盖伦至臻版']
	rd[30][0] = ['奥德赛：为自己和邻格奥德赛英雄提','供护盾(持续6s)和伤害提升效果','(2)：150点护盾值和10%伤害提升','(3)：200点护盾值和20%伤害提升']
	rd[30][1] = [[150,0.1],[200,0.2],6]
	rd[31][0] = ['未来战士：全队每4s获得攻速加成','(2)：15%攻击速度','(3)：25%攻击速度']
	rd[31][1] = [0.15,0.25,4]
	rd[32][0] = ['星神：所有友军的普攻和技能造成伤','害时，获得一部分伤害值的治疗效果','(2)：25%治疗效果','(3)：50%治疗效果']
	rd[32][1] = [0.25,0.5]
	rd[33][0] = ['星之守护者：施法技能时为其他星之','守护者提供法力值','(2)：提供30法力值','(3)：提供40法力值']
	rd[33][1] = [30,40]
	rd[34][0] = ['暗星：每有1个英雄死亡，产生1层暗','星能量(若为己方暗星英雄则翻倍)','(2)：每1层暗星能量，提升40%伤害','(3)：每1层暗星能量，提升80%伤害']
	rd[34][1] = [0.4,0.8]
	rd[35][0] = ['爆破专家：技能对目标造成伤害时眩','晕目标，每次技能只触发一次眩晕','(2)：眩晕2s','(3)：眩晕4s']
	rd[35][1] = [2,4]
	rd[36][0] = ['源计划：从两件基础武器中获得额外','属性，并且部分进阶武器会获得升级','(2)：基础武器属性×2','(3)：基础武器属性×3']
	rd[36][1] = [2,3]
	rd[37][0] = ['护卫：提升自身和周围队友的护甲','(2)：自身+50护甲，周围队友+25护甲','(3)：自身+80护甲，周围队友+40护甲']
	rd[37][1] = [[50,25],[80,40]]
	rd[38][0] = ['星舰龙神：每秒获得10点法力值，免','疫控制效果，但无法进行普通攻击']
	rd[39][0] = ['虚空：虚空单位造成真实伤害']
	rd[40][0] = ['先锋：先锋单位会嘲讽周围的敌人']
	rd[41][0] = ['银河魔装机神：由银河机神合体而成，','在死亡时解体','拥有专属武器—巨型九头蛇']
	rd[42][0] = ['异星人：每有1个存活的友方单位，获','得10%减伤(上限90%)、10%法强；友方','单位：英雄、炮台、皮克斯、提伯斯、','虚空兽、机神盖伦、已出舱的战斗机']

	rela_dic = {'光' : rd[0], '极地' : rd[1], '森林' : rd[2], '水晶' : rd[3], '海洋' : rd[4], '钢铁' : rd[5], '沙漠' : rd[6], \
	'游侠' : rd[7], '掠食者' : rd[8], '秘术师' : rd[9], '守护神' : rd[10], '法师' : rd[11], '刺客' : rd[12], '狂战士' : rd[13],\
	 '大元素使' : rd[14], '地狱火' : rd[15], '影' : rd[16], '黯焰' : rd[17], '恕瑞玛之皇' : rd[18], '太阳圆盘' : rd[19], \
	 '斗士' : rd[20], '银月' : rd[21], '剧毒' : rd[22], '剑士' : rd[23], '枪手' : rd[24], '云霄' : rd[25], '雷霆' : rd[26], \
	 '忍者' : rd[27], '忍剑士' : rd[28], '银河机神' : rd[29], '奥德赛' : rd[30], '未来战士' : rd[31], '星神' : rd[32], \
	 '星之守护者' : rd[33], '暗星' : rd[34], '爆破专家' : rd[35], '源计划' : rd[36], '护卫' : rd[37], '星舰龙神' : rd[38], \
	 '虚空' : rd[39], '先锋' : rd[40], '银河魔装机神' : rd[41], '异星人' : rd[42]}

class Tide(object):
	def __init__(self,Nami = None,flag = False):
		self.Nami = Nami 											# 施法者：娜美
		self.flag = False 											# 水潮存在标志
		self.time_count = Time_count() 								# 计算间隔时间
		self.target = None 											# 水潮目标
		self.target_number = 1 										# 水潮目标编号
		self.target_deal_finish_flag = [False,False]          		# 第一/二个目标处理结束标志
		self.interval_end_flag = [False,False]            			# 第一/二段间隔时间结束标志
		self.pass_flag = False 										# 直接跳到第二个目标的标志
	# 水潮流动
	def Flow(self):
		# 施法到第一个目标不需要间隔时间
		# 水潮的第一个目标：除娜美外生命值最低的友方，若友方死亡或处于不可选取状态，则直接跳到第二个目标(不计间隔时间)
		if self.target_number == 1:
			if not self.target_deal_finish_flag[0]:
				# 判断目标
				if self.Nami.flag.special_flag.dead_area[0]:
					self.target_number = 2
					self.target_deal_finish_flag[0] = True
					self.interval_end_flag[0] = True
					self.pass_flag = True
				else:
					hp_min = 10000
					friend_pos_number = 0
					for i in range(3):
						if (self.Nami.friend[i] != self.Nami) and (not self.Nami.friend[i].flag.condition_flag.death_flag) and (not self.Nami.friend[i].flag.condition_flag.miss_flag[0]) \
						and (not self.Nami.friend[i].flag.special_flag.dead_area[0]) and (self.Nami.friend[i].champion.hp.value + self.Nami.friend[i].condition.shield.value) <= hp_min:
							hp_min = self.Nami.friend[i].champion.hp.value + self.Nami.friend[i].condition.shield.value
							friend_pos_number = i
					if hp_min == 10000:
						self.target_number = 2
						self.target_deal_finish_flag[0] = True
						self.interval_end_flag[0] = True
						self.pass_flag = True
					else:
						value_treatment1 = self.Nami.champion.skill.para[0] * self.Nami.champion.attack_attribute.spell_power
						self.Nami.friend[friend_pos_number].champion.hp.HP_restore(value_treatment1,self.Nami.champion,self.Nami.friend[friend_pos_number])
						if self.Nami.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
							self.Nami.condition.fervor.Add_fervor(self.Nami.friend[friend_pos_number],self.Nami.flag.weapon_flag.crxl[2][2])
							self.Nami.flag.weapon_flag.crxl[3] = True
						self.Nami.friend[friend_pos_number].flag.special_flag.effect[self.Nami.champion.skill.name][0] = True
						self.target_deal_finish_flag[0] = True
		# 第一段间隔时间
		self.Interval(1)
		# 水潮的第二个目标：随机一名敌人，若此时敌人死亡或不可选取，则水潮流动结束，若触发敌人的伏击之爪或者魔法护盾，则水潮流动结束
		if self.target_number == 2:
			if not self.target_deal_finish_flag[1]:
				# 判断目标
				if self.Nami.flag.special_flag.dead_area[0]:
					enemy = self.Nami.flag.special_flag.dead_area[1]
				else:
					enemy_pos_number = randint(0,2)
					enemy = None
					for i in range(3):
						if (not self.Nami.game.LR[~self.Nami.position+2][enemy_pos_number].flag.condition_flag.death_flag) and (not self.Nami.game.LR[~self.Nami.position+2][enemy_pos_number].flag.condition_flag.miss_flag[0]):
							enemy = self.Nami.game.LR[~self.Nami.position+2][enemy_pos_number]
							break
						else:
							enemy_pos_number += 1
							if enemy_pos_number == 3:
								enemy_pos_number = 0
				if enemy == None:
					self.__init__()
				else:
					# 处理敌人魔法护盾效果
					if enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
						enemy.flag.condition_flag.buff_magic_shield_flag = False
						self.__init__()
					elif enemy.flag.weapon_flag.fjzz[0] and enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果，不是直接向敌人施法则不受眩晕效果
						enemy.flag.weapon_flag.fjzz[1] = False
						if (not self.Nami.flag.condition_flag.death_flag) and (not self.Nami.flag.condition_flag.miss_flag[0]) \
						and (not self.Nami.flag.condition_flag.buff_invincible_flag) and (not self.Nami.flag.condition_flag.buff_unstoppable_flag) \
						and self.pass_flag:
							dizz_time = enemy.flag.weapon_flag.fjzz[2] / self.Nami.champion.defensive_attribute.tenacity
							self.Nami.condition.dizz.Add_dizz(self.Nami,dizz_time)
						self.__init__()
					else:
						self.Nami.champion.attack_attribute.spell_attack.spell_damage = (self.Nami.champion.skill.para[1][0] + self.Nami.champion.skill.para[1][1] * \
							self.Nami.champion.defensive_attribute.spell_resistance) * self.Nami.champion.attack_attribute.spell_power
						# 计算技能伤害
						self.Nami.Spell_attack_damage_calculation()
						enemy.flag.special_flag.effect[self.Nami.champion.skill.name][0] = True
						if (not self.Nami.flag.condition_flag.death_flag) and (not self.Nami.flag.condition_flag.miss_flag[0]) and \
						self.Nami.flag.weapon_flag.ldhs[0] and self.Nami.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
							self.Nami.flag.weapon_flag.ldhs[1] = True
							self.Nami.flag.weapon_flag.ldhs[4] = enemy
						self.target_deal_finish_flag[1] = True
		# 第二段间隔时间
		self.Interval(2)
		# 水潮的第三个目标：娜美自己，若此时娜美死亡或不可选取，则水潮流动结束
		if self.target_number == 3:
			if (not self.Nami.flag.condition_flag.death_flag) and (not self.Nami.flag.condition_flag.miss_flag[0]):
				value_treatment2 = self.Nami.champion.skill.para[0] * self.Nami.champion.attack_attribute.spell_power
				self.Nami.champion.hp.HP_restore(value_treatment2,self.Nami.champion,self.Nami)
				if (not self.Nami.flag.condition_flag.death_flag) and (not self.Nami.flag.condition_flag.miss_flag[0]) and self.Nami.flag.weapon_flag.crxl[0]: 	# 触发炽热香炉效果
					self.Nami.condition.fervor.Add_fervor(self.Nami,self.Nami.flag.weapon_flag.crxl[2][2])
					self.Nami.flag.weapon_flag.crxl[3] = True
				self.Nami.flag.special_flag.effect[self.Nami.champion.skill.name][0] = True
				self.__init__()
			else:
				self.__init__()
	# 间隔时间处理
	def Interval(self,i):
		if self.target_deal_finish_flag[i-1] and not self.interval_end_flag[i-1]:
			self.interval_end_flag[i-1] = self.time_count.Duration(self.Nami.champion.skill.para[2])
			if self.interval_end_flag[i-1]:
				self.target_number = i+1
tide = Tide()
# 布兰德释放的火球
class Fireball(object):
	def __init__(self,Brand = None,flag = False,enemy = None):
		self.Brand = Brand 											# 施法者：布兰德
		self.flag = False 											# 火球存在标志
		self.time_count = Time_count() 								# 计算间隔时间
		self.number = 1 											# 火球弹跳计数
		self.deal_finish_flag = [False for _ in range(5)]         	# 处理结束标志
		self.interval_end_flag = [True]+[False for _ in range(4)]  	# 间隔时间结束标志
		self.enemy = enemy 											# 上一个目标
		self.count = {0 : 0, 1 : 0, 2 : 0}							# 敌人命中火球计数值
	# 火球跳动
	def Jump(self):
		# 第一个目标
		if self.number == 1:
			self.Deal(1)
		# 第一段间隔时间
		self.Interval(1)
		# 第二个目标
		if self.number == 2:
			self.Deal(2)
		# 第二段间隔时间
		self.Interval(2)
		# 第三个目标
		if self.number == 3:
			self.Deal(3)
		# 第三段间隔时间
		self.Interval(3)
		# 第四个目标
		if self.number == 4:
			self.Deal(4)
		# 第四段间隔时间
		self.Interval(4)
		# 第五个目标
		if self.number == 5:
			self.Deal(5)
			self.__init__()
	# 处理
	def Deal(self,i):
		if not self.deal_finish_flag[i-1] and self.interval_end_flag[i-1]:
			# 判断目标
			# 	火球的第一个目标是布兰德的攻击对象;后续目标：随机敌人(不处于死亡状态和不可选取状态)，且与前一目标不重复
			if self.number != 1:
				enemy_pos_number = randint(0,2)
				enemy = None
				for _ in range(3):
					if (not self.Brand.game.LR[~self.Brand.position+2][enemy_pos_number].flag.condition_flag.death_flag) \
					and (not self.Brand.game.LR[~self.Brand.position+2][enemy_pos_number].flag.condition_flag.miss_flag[0])\
					and (not self.Brand.game.LR[~self.Brand.position+2][enemy_pos_number].flag.special_flag.dead_area[0])\
					and (not self.Brand.game.LR[~self.Brand.position+2][enemy_pos_number] == self.enemy):
						enemy = self.Brand.game.LR[~self.Brand.position+2][enemy_pos_number]
						self.enemy = enemy
						break
					else:
						enemy_pos_number += 1
						if enemy_pos_number == 3:
							enemy_pos_number = 0
			else:
				enemy = self.enemy
			if self.Brand.champion.skill.para[3]:
				if self.number != 1:
					enemy = None
			# 失去目标则停止
			if enemy == None:
				self.__init__()
			# 技能判定与伤害计算
			else:
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					self.__init__()
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果，不是直接向敌人施法则不受眩晕效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if (not self.Brand.flag.condition_flag.death_flag) and (not self.Brand.flag.condition_flag.miss_flag[0]) \
					and (not self.Brand.flag.condition_flag.buff_invincible_flag) and (not self.Brand.flag.condition_flag.buff_unstoppable_flag)\
					and self.number == 1:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.Brand.champion.defensive_attribute.tenacity
						self.Brand.condition.dizz.Add_dizz(self.Brand,dizz_time)
					self.__init__()
				else:
					temp_enemy = self.Brand.enemy
					self.Brand.enemy = self.enemy
					self.Brand.champion.attack_attribute.spell_attack.spell_damage = self.Brand.champion.skill.para[0] * self.Brand.champion.attack_attribute.spell_power
					# 计算技能伤害
					self.Brand.Spell_attack_damage_calculation()
					# 命中次数计数
					self.count[self.enemy.pos_num] += 1
					# 命中3次则眩晕3s
					if self.count[self.enemy.pos_num] == 3:
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.Brand.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
							self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
							self.Brand.champion.skill.para[4] += 1
							self.Brand.champion.skill.extra[2][0][2] = True
					self.enemy.flag.special_flag.effect[self.Brand.champion.skill.name][0] = True
					if (not self.Brand.flag.condition_flag.death_flag) and (not self.Brand.flag.condition_flag.miss_flag[0]) and \
					self.Brand.flag.weapon_flag.ldhs[0] and self.Brand.flag.damage_calculation_flag.spell_attack and self.number == 1: 	# 触发卢登回声效果
						self.Brand.flag.weapon_flag.ldhs[1] = True
						self.Brand.flag.weapon_flag.ldhs[4] = self.enemy
					self.Brand.enemy = temp_enemy
					# 处理结束
					self.deal_finish_flag[i-1] = True
	# 间隔时间处理
	def Interval(self,i):
		if self.deal_finish_flag[i-1] and not self.interval_end_flag[i]:
			self.interval_end_flag[i] = self.time_count.Duration(self.Brand.champion.skill.para[2])
			if self.interval_end_flag[i]:
				self.number = i+1
fireball = Fireball()
# 拉克丝掷出的魔杖
class Wand(object):
	def __init__(self,Lux = None,flag = False,mode = 0):
		self.Lux = Lux 												# 施法者：拉克丝
		self.flag = False 											# 魔杖存在标志
		self.time_count = Time_count() 								# 计算间隔时间
		self.target = None 											# 魔杖目标
		self.target_number = 1 										# 魔杖目标编号
		self.target_deal_finish_flag = [False for _ in range(5)]    # 目标处理结束标志
		self.interval_end_flag = [False for _ in range(5)]       	# 间隔时间结束标志
		self.interval_time = [0.5,1,0] 								# 间隔时间|折返时间|选项
		self.mode = mode 											# 三种情形
		self.finish_flag = False 									# 结束标志
	# 魔杖飞行：若拉克丝在端部，则朝最远队友(最多6个目标)，若拉克丝在中间，随机朝一个方向(最多4个目标)
	def Fly(self):
		# 第一个目标(self)不需要间隔时间
		# 第一个目标：拉克丝自己
		if self.target_number == 1:
			if not self.target_deal_finish_flag[0]:
				self.target = self.Lux
				self.Parclose()
				self.target_deal_finish_flag[0] = True
		# 第一段间隔时间
		self.Interval(1,self.interval_time[2])
		# 第二个目标
		if self.target_number == 2:
			if not self.target_deal_finish_flag[1]:
				# 判断目标
				if self.mode == 1:
					temp = [0,2]
					temp_target_num = 0
					if (self.Lux.game.LR[self.Lux.position][0].champion.hp.value + self.Lux.game.LR[self.Lux.position][0].condition.shield.value)\
					 > (self.Lux.game.LR[self.Lux.position][2].champion.hp.value + self.Lux.game.LR[self.Lux.position][2].condition.shield.value)\
					 and (not self.Lux.game.LR[self.Lux.position][2].flag.condition_flag.death_flag and not self.Lux.game.LR[self.Lux.position][2].flag.condition_flag.miss_flag[0]):
						temp_target_num = 1
					elif self.Lux.game.LR[self.Lux.position][0].flag.condition_flag.death_flag or self.Lux.game.LR[self.Lux.position][0].flag.condition_flag.miss_flag[0]:
						temp_target_num = 1
					self.target = self.Lux.game.LR[self.Lux.position][temp[temp_target_num]]
					self.interval_time[2] = 1
				else:
					self.target = self.Lux.game.LR[self.Lux.position][1]
				# 获得护盾
				self.Parclose()
				self.target_deal_finish_flag[1] = True
		# 第二段间隔时间，mode = 1时为折返时间
		self.Interval(2,self.interval_time[2])
		# 第三个目标
		if self.target_number == 3:
			if not self.target_deal_finish_flag[2]:
				# 判断目标
				if self.mode == 1:
					self.target = self.target
					self.interval_time[2] = 0
				elif self.mode == 0:
					self.target = self.Lux.game.LR[self.Lux.position][2]
					self.interval_time[2] = 1
				else:
					self.target = self.Lux.game.LR[self.Lux.position][0]
					self.interval_time[2] = 1
				# 获得护盾
				self.Parclose()
				self.target_deal_finish_flag[2] = True
		# 第三段间隔时间，mode = 1时为折返时间
		self.Interval(3,self.interval_time[2])
		# 第四个目标
		if self.target_number == 4:
			if not self.target_deal_finish_flag[3]:
				# 判断目标
				if self.mode == 1:
					self.target = self.Lux
					self.finish_flag = True
				else:
					self.target = self.target
					self.interval_time[2] = 0
				# 获得护盾
				self.Parclose()
				if self.finish_flag:
					self.__init__()
				else:
					self.target_deal_finish_flag[3] = True
		# 第四段间隔时间
		self.Interval(4,self.interval_time[2])
		# 第五个目标
		if self.target_number == 5:
			if not self.target_deal_finish_flag[4]:
				# 判断目标
				self.target = self.Lux.game.LR[self.Lux.position][1]
				# 获得护盾
				self.Parclose()
				self.target_deal_finish_flag[4] = True
		# 第五段间隔时间
		self.Interval(5,self.interval_time[2])
		# 第六个目标
		if self.target_number == 6:
			# 判断目标
			self.target = self.Lux
			# 获得护盾
			self.Parclose()
			self.__init__()
	# 获得屏障
	def Parclose(self):
		if not((self.Lux.flag.special_flag.dead_area[0] and self.target != self.Lux) or ((not self.Lux.flag.special_flag.dead_area[0]) and self.target.flag.special_flag.dead_area[0])):
			# 获得护盾
			if not self.target.flag.condition_flag.death_flag and not self.target.flag.condition_flag.miss_flag[0]:
				shield_add = self.Lux.champion.skill.para[1][0] * self.Lux.champion.attack_attribute.spell_power
				self.Lux.condition.shield.Add_shield(self.target,shield_add,self.Lux.champion.skill.para[1][1])
				if self.Lux.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
					self.Lux.condition.fervor.Add_fervor(self.target,self.Lux.flag.weapon_flag.crxl[2][2])
					self.Lux.flag.weapon_flag.crxl[3] = True
				self.target.flag.special_flag.effect['曲光屏障'][0] = True
	# 间隔时间处理
	def Interval(self,i,j):
		if self.target_deal_finish_flag[i-1] and not self.interval_end_flag[i-1]:
			self.interval_end_flag[i-1] = self.time_count.Duration(self.interval_time[j])
			if self.interval_end_flag[i-1]:
				self.target_number = i+1
wand = Wand()
# 阿兹尔召唤的沙兵
class Sand(object):
	def __init__(self,Azir = None):
		self.Azir = Azir
		self.flag = False
		self.position = 0
		self.pos_num = 0
		self.time_count = Time_count()
		self.enemy = None
	# 沙兵攻击(能被魔法护盾和伏击之爪格挡，但阿兹尔不会受到伏击之爪的眩晕效果);沙兵不触发卢登
	def Attack(self):
		if not self.Azir.game.LR[~self.position+2][self.pos_num].flag.condition_flag.death_flag and not self.Azir.game.LR[~self.position+2][self.pos_num].flag.condition_flag.miss_flag[0]\
		and not (self.Azir.flag.special_flag.dead_area[0] ^ self.Azir.game.LR[~self.position+2][self.pos_num].flag.special_flag.dead_area[0])\
		and not (self.Azir.flag.special_flag.dead_area[0] and (self.pos_num != self.Azir.flag.special_flag.dead_area[1].pos_num)):
			self.enemy = self.Azir.game.LR[~self.position+2][self.pos_num]
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
			else:
				self.Azir.champion.attack_attribute.spell_attack.spell_damage = self.Azir.champion.skill.para[0] * self.Azir.champion.attack_attribute.spell_power
				# 计算技能伤害
				temp_enemy = self.Azir.enemy
				self.Azir.enemy = self.enemy
				self.Azir.Spell_attack_damage_calculation()
				self.enemy.flag.special_flag.effect['沙兵攻击'][0] = True
				self.Azir.enemy = temp_enemy
sand = [Sand(),Sand(),Sand()]
for i in range(3):
	sand[i].pos_num = i
# 伙伴(魔偶/皮克斯)坐标
partner_xy = [[[223,105],[223,335],[223,565]],[[938,105],[938,335],[938,565]]]
# 奥莉安娜的魔偶
class Golem(object):
	def __init__(self,Orianna = None):
		self.Orianna = Orianna
		self.flag = False                   						# 存在标志
		self.moving_flag = False									# 移动中状态
		self.time = [0.5,2]
		self.time_count = [Time_count(),Time_count()]
		self.position = 0
		self.pos_num = 0
		self.start_point = [0,0]								 	# 起点
		self.end_point = [0,0] 										# 终点
		self.current_point = self.start_point 						# 当前位置	
		self.frame_number = [0,20]									# 帧数
		self.delta = [0,0]											# 每帧位移
		self.target = None
		self.mode = 0 												# 移动模式，1：敌军/友军到友军，2：友军/敌军到敌军(1格)，3：敌军到敌军(2格)
		self.friend_pos_number = 3
		self.defend = [False,None]
	# 初始化起点
	def Init(self):
		for i in range(2):
			self.start_point[i] = partner_xy[self.position][self.pos_num][i]
		self.current_point = self.start_point
	# 选择目标函数
	def Target1(self,a,b,c):
		if not self.Orianna.game.LR[~self.Orianna.position+2][a].flag.condition_flag.death_flag \
		and not self.Orianna.game.LR[~self.Orianna.position+2][a].flag.condition_flag.miss_flag[0]:
			self.target = self.Orianna.game.LR[~self.Orianna.position+2][a]
			self.mode = 2
		# 若该目标不可选取则改为随机一个可选取的敌人
		else:
			target = [self.Orianna.game.LR[~self.Orianna.position+2][b],self.Orianna.game.LR[~self.Orianna.position+2][c]]
			e2 = randint(0,1)
			if not target[e2].flag.condition_flag.death_flag and not target[e2].flag.condition_flag.miss_flag[0]:
				self.target = target[e2]
				self.mode = 2
			elif not target[~e2+2].flag.condition_flag.death_flag and not target[~e2+2].flag.condition_flag.miss_flag[0]:
				self.target = target[~e2+2]
				self.mode = 2
			else:	
				self.target = self.Orianna
				self.mode = 1
	def Target2(self,a,b):
		if not self.Orianna.game.LR[~self.Orianna.position+2][a].flag.condition_flag.death_flag \
		and not self.Orianna.game.LR[~self.Orianna.position+2][a].flag.condition_flag.miss_flag[0]:
			self.target = self.Orianna.game.LR[~self.Orianna.position+2][a]
		elif not self.Orianna.game.LR[~self.Orianna.position+2][b].flag.condition_flag.death_flag \
		and not self.Orianna.game.LR[~self.Orianna.position+2][b].flag.condition_flag.miss_flag[0]:
			self.target = self.Orianna.game.LR[~self.Orianna.position+2][b]
		else:
			self.target = self.Orianna.friend[self.friend_pos_number]
	# 根据起点随机确定终点
	def Judg_end_point(self):
		e = randint(0,99)
		hp_min = self.Orianna.champion.hp.value + self.Orianna.condition.shield.value
		self.friend_pos_number = 3
		for i in range(3):
			if (not self.Orianna.friend[i].flag.condition_flag.death_flag) and (not self.Orianna.friend[i].flag.condition_flag.miss_flag[0]) \
			and (self.Orianna.friend[i].champion.hp.value + self.Orianna.friend[i].condition.shield.value) <= hp_min:
				hp_min = self.Orianna.friend[i].champion.hp.value + self.Orianna.friend[i].condition.shield.value
				self.friend_pos_number = i
			if self.friend_pos_number == 3:
				self.friend_pos_number = self.Orianna.pos_num
		# 情形1：起点是友方，则终点30%几率为敌方1号位，40%几率为敌方2号位，30%几率为敌方3号位
		if self.position == self.Orianna.position:
			if e < 30:
				self.Target1(0,1,2)
			elif e < 70:
				self.Target1(1,0,2)
			else:
				self.Target1(2,0,1)
		# 情形2：起点是敌方中心位置，则终点30%几率为敌方1号位，40%几率为生命值最低友方，30%几率为敌方3号位
		elif self.position != self.Orianna.position and self.pos_num == 1:
			if e < 30:
				self.Target2(0,2)
				if not self.target == self.Orianna.friend[self.friend_pos_number]:
					self.mode = 2
				else:
					self.mode = 1
			elif e < 70:
				self.target = self.Orianna.friend[self.friend_pos_number]
				self.mode = 1
			else:
				self.Target2(2,0)
				if not self.target == self.Orianna.friend[self.friend_pos_number]:
					self.mode = 2
				else:
					self.mode = 1
		# 情形3：起点是敌方边缘位置，则终点40%几率为敌方另一个边缘位置，30%几率为敌方中心位置，30%几率为生命值最低友方
		else:
			if e < 40:
				if self.pos_num == 0:
					self.Target2(2,1)
					if self.target == self.Orianna.game.LR[~self.Orianna.position+2][2]:
						self.mode = 3
					elif self.target == self.Orianna.game.LR[~self.Orianna.position+2][1]:
						self.mode = 2
					else:
						self.mode = 1
				else:
					self.Target2(0,1)
					if self.target == self.Orianna.game.LR[~self.Orianna.position+2][0]:
						self.mode = 3
					elif self.target == self.Orianna.game.LR[~self.Orianna.position+2][1]:
						self.mode = 2
					else:
						self.mode = 1
			elif e < 70:
				if self.pos_num == 0:
					self.Target2(1,2)
					if self.target == self.Orianna.game.LR[~self.Orianna.position+2][1]:
						self.mode = 2
					elif self.target == self.Orianna.game.LR[~self.Orianna.position+2][2]:
						self.mode = 3
					else:
						self.mode = 1
				else:
					self.Target2(1,0)
					if self.target == self.Orianna.game.LR[~self.Orianna.position+2][1]:
						self.mode = 2
					elif self.target == self.Orianna.game.LR[~self.Orianna.position+2][0]:
						self.mode = 3
					else:
						self.mode = 1
			else:
				self.target = self.Orianna.friend[self.friend_pos_number]
				self.mode = 1
		for i in range(2):
			self.end_point[i] = partner_xy[self.target.position][self.target.pos_num][i]
		# 计算位移
		for i in range(2):
			self.delta[i] = int((self.end_point[i] - self.start_point[i])/self.frame_number[1])
	# 魔偶移动中
	def Moving(self):
		end_flag1 = self.time_count[0].Duration(self.time[0]/self.frame_number[1])
		if end_flag1:
			# 当前位置变化
			for i in range(2):
				self.current_point[i] += self.delta[i]
			self.frame_number[0] += 1
			if self.frame_number[0] == self.frame_number[1]:
				# 计算伤害
				self.Damage()
				# 进入停留状态
				self.position = self.target.position
				self.pos_num = self.target.pos_num
				self.Init()
				self.frame_number[0] = 0
				self.moving_flag = False 
	# 计算伤害
	def Damage(self):
		# 计算技能伤害；魔偶的伤害不能被魔法护盾和伏击之爪抵挡
		self.Orianna.champion.attack_attribute.spell_attack.spell_damage = self.Orianna.champion.skill.para[0] * self.Orianna.champion.attack_attribute.spell_power
		temp_enemy = self.Orianna.enemy
		if self.mode == 3:
			self.Orianna.enemy = self.Orianna.game.LR[~self.Orianna.position+2][1]
			if not self.Orianna.enemy.flag.condition_flag.death_flag and not self.Orianna.enemy.flag.condition_flag.miss_flag[0]:
				self.Orianna.Spell_attack_damage_calculation()
				self.Orianna.enemy.flag.special_flag.effect['魔偶攻击'][0] = True
		if self.mode != 1:
			self.Orianna.enemy = self.target
			if not self.Orianna.enemy.flag.condition_flag.death_flag and not self.Orianna.enemy.flag.condition_flag.miss_flag[0]:
				self.Orianna.Spell_attack_damage_calculation()
				self.Orianna.enemy.flag.special_flag.effect['魔偶攻击'][0] = True
		self.Orianna.enemy = temp_enemy
	# 魔偶主程序
	def Move(self):
		if not self.Orianna.flag.condition_flag.miss_flag[0]:
			# 移动中
			if self.moving_flag:
				self.Moving()
			else:
				end_flag2 = self.time_count[1].Duration(self.time[1])
				if end_flag2:
					# 恢复双抗加成
					if self.defend[0]:
						self.defend[1].champion.defensive_attribute.armor -= self.Orianna.champion.skill.para[1][2]
						if self.defend[1].champion.defensive_attribute.armor == 0:
							self.defend[1].champion.defensive_attribute.armor = 0
						self.defend[1].champion.defensive_attribute.spell_resistance -= self.Orianna.champion.skill.para[1][3]
						if self.defend[1].champion.defensive_attribute.spell_resistance == 0:
							self.defend[1].champion.defensive_attribute.spell_resistance = 0
						self.defend[0] = False
					# 判断终点
					self.Judg_end_point()
					# 进入移动状态
					self.moving_flag = True
					self.Orianna.champion.skill.extra[2][0][2] = True
				else:
					# 为附属友军提供双抗
					if self.position == self.Orianna.position and not self.defend[0]:
						self.defend[1] = self.Orianna.game.LR[self.position][self.pos_num]
						self.defend[1].champion.defensive_attribute.armor += self.Orianna.champion.skill.para[1][2]
						self.defend[1].champion.defensive_attribute.spell_resistance += self.Orianna.champion.skill.para[1][3]
						self.defend[0] = True
golem = Golem()
# 厄斐琉斯部署的月之驻灵
class MoonBattery(object):
	def __init__(self,Aphelios = None,weapon_num = 0):
		self.Aphelios = Aphelios
		self.flag = False
		self.position = 0
		self.pos_num = 0
		self.normal_attack_time_count = 0
		self.attack_speed = 0.7
		self.time_count = [Time_count(),Time_count()] 	# 持续时间计数|普攻间隔计数
		self.time = 9
		self.weapon_num = weapon_num
		self.enemy = None
	# 驻灵攻击(能被魔法护盾和伏击之爪格挡，但厄斐琉斯不会受到伏击之爪的眩晕效果);驻灵不触发卢登
	def Attack(self):
		# 持续时间判断
		exist_flag = self.Continue()
		if exist_flag:
			self.normal_attack_time_count += 1
			if self.normal_attack_time_count >= int((1 / self.attack_speed * 100) / time_correction[0]):
				# 普攻间隔时间计数值清零
				self.normal_attack_time_count = 0
				self.enemy = self.Aphelios.game.LR[~self.position+2][self.pos_num]
				if not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
					# 敌人闪避判断
					dodge_flag = self.Aphelios.champion.defensive_attribute.dodge_mechanism.Dodge_judg(self.enemy) and not self.enemy.flag.condition_flag.debuff_dizz_flag \
					and not self.enemy.flag.condition_flag.debuff_frozen_flag and not self.enemy.flag.condition_flag.suppress[0]
					# 计算伤害
					if not dodge_flag:
						# 驻灵攻击标志置位
						self.Aphelios.champion.skill.para[4][2] = True
						temp_enemy = self.Aphelios.enemy
						self.Aphelios.enemy = self.enemy
						# 暂时将主武器设为驻灵的武器属性
						self.Aphelios.mwd_dic[self.Aphelios.moon_weapon[self.Aphelios.weapon_seq[0]][0]][1] = False
						self.Aphelios.mwd_dic[self.Aphelios.moon_weapon[self.weapon_num][0]][1] = True
						# 驻灵攻击即为追加攻击
						self.Aphelios.Additional_attack()
						# 显示
						self.enemy.flag.special_flag.effect['月之驻灵'][0] = True
						# 复原
						self.Aphelios.mwd_dic[self.Aphelios.moon_weapon[self.weapon_num][0]][1] = False
						self.Aphelios.mwd_dic[self.Aphelios.moon_weapon[self.Aphelios.weapon_seq[0]][0]][1] = True
						self.Aphelios.enemy = temp_enemy
						# 驻灵攻击标志清除
						self.Aphelios.champion.skill.para[4][2] = False
	# 持续时间计算
	def Continue(self):
		if self.time_count[0].Duration(self.time):
			self.flag = False
			return False
		else:
			return True
	# 初始化
	def Init(self):
		self.normal_attack_time_count = 0
		self.time_count[1].value = 0
moonbattery = [MoonBattery(),MoonBattery(),MoonBattery()]
for i in range(3):
	moonbattery[i].pos_num = i
# 皮克斯
class Pix(object):
	def __init__(self,Lulu = None):
		self.Lulu = Lulu
		self.flag = False                   						# 存在标志
		self.moving_flag = False									# 移动中状态
		self.time = [0.5,5,2] 										# 飞行时间|在队友身上停留时间|在敌人身上停留时间
		self.time_count = [Time_count(),Time_count()]
		self.position = 0
		self.pos_num = 0
		self.start_point = [0,0]								 	# 起点
		self.end_point = [0,0] 										# 终点
		self.current_point = self.start_point 						# 当前位置	
		self.frame_number = [0,20]									# 帧数
		self.delta = [0,0]											# 每帧位移
		self.target = None 											# 当前目标

	# 初始化起点
	def Init(self):
		for i in range(2):
			self.start_point[i] = partner_xy[self.position][self.pos_num][i]
		self.current_point = self.start_point
	# 选择目标
	def Target_enemy(self,mode): 	# mode = 0表示情形1，mode = 1表示情形2，mode = 2表示找不到友军转为敌人
		# 随机一个敌人
		p = randint(0,2)
		self.target = self.Lulu.game.LR[~self.Lulu.position+2][p]
		i = 3
		while i >= 0:
			if not self.Lulu.game.LR[~self.Lulu.position+2][p].flag.condition_flag.death_flag and not self.Lulu.game.LR[~self.Lulu.position+2][p].flag.condition_flag.miss_flag[0]:
				if mode == 0:
					self.target = self.Lulu.game.LR[~self.Lulu.position+2][p]
					break
				elif mode == 1:
					if self.Lulu.game.LR[~self.Lulu.position+2][p] != self.target:
						self.target = self.Lulu.game.LR[~self.Lulu.position+2][p]
						break
					else:
						p += 1
						if p == 3:
							p = 0
			else:
				p += 1
				if p == 3:
					p = 0
			i -= 1
		if i < 0:					# 即此时敌人处于于不可选取状态，则改为选择一生命值较低的友方
			if mode == 2:
				self.target = self.Lulu
			else:
				self.Target_friend(2)
	def Target_friend(self,mode):	# mode = 0表示情形1，mode = 1表示情形2，mode = 2表示找不到敌人时转为友军
		# 队友生命值排序
		hp_seq = [self.Lulu.friend[i] for i in range(3)]
		for i in range(2):
			for j in range(2-i):
				if hp_seq[j+1].champion.hp.value < hp_seq[j].champion.hp.value:
					temp = hp_seq[j]
					hp_seq[j] = hp_seq[j+1]
					hp_seq[j+1] = temp
		temp_target = self.target
		for i in range(3):
			if not hp_seq[i].flag.condition_flag.death_flag and not hp_seq[i].flag.condition_flag.miss_flag[0]:
				if mode == 0:
					if hp_seq[i] != self.target:
						self.target = hp_seq[i]
						break
				elif mode == 1:
					self.target = hp_seq[i]
					break
		if self.target == temp_target:
			if mode == 2:
				self.target == self.Lulu
			else:
				self.Target_enemy(2)
	# 根据起点随机确定终点
	def Judg_end_point(self):
		e = randint(0,99)
		# 情形1：起点是友方，则终点60%为另一个生命值较低的友方，40%是随机一个敌人
		if self.position == self.Lulu.position:
			if e < 40:
				self.Target_enemy(0)
			else:
				self.Target_friend(0)
		# 情形2：起点是敌方，则终点75%是生命值较低的友方，25%是随机另一个敌人
		elif self.position != self.Lulu.position:
			if e < 25:
				self.Target_enemy(1)
			else:
				self.Target_friend(1)
		for i in range(2):
			self.end_point[i] = partner_xy[self.target.position][self.target.pos_num][i]
		# 计算位移
		for i in range(2):
			self.delta[i] = int((self.end_point[i] - self.start_point[i])/self.frame_number[1])
	# 皮克斯移动中
	def Moving(self):
		end_flag1 = self.time_count[0].Duration(self.time[0]/self.frame_number[1])
		if end_flag1:
			# 当前位置变化
			for i in range(2):
				self.current_point[i] += self.delta[i]
			self.frame_number[0] += 1
			if self.frame_number[0] == self.frame_number[1] or (self.delta[0] == 0 and self.delta[1] == 0):
				# 进入停留状态
				self.position = self.target.position
				self.pos_num = self.target.pos_num
				self.Init()
				self.frame_number[0] = 0
				self.moving_flag = False 
	# 皮克斯攻击，属于技能伤害且不会被格挡，也不会触发羁绊和武器的效果
	def Attack(self):
		temp_enemy = self.Lulu.enemy
		self.Lulu.enemy = self.target.enemy
		# 显示
		self.target.enemy.flag.special_flag.effect['皮克斯攻击'][0] = True
		self.Lulu.champion.attack_attribute.spell_attack.spell_damage = self.Lulu.champion.skill.para[2] * self.Lulu.champion.attack_attribute.spell_power
		# 伤害计算
		self.Lulu.Spell_attack_damage_calculation()
		self.Lulu.enemy = temp_enemy
	# 皮克斯主程序
	def Move(self):
		# 移动中
		if self.moving_flag:
			self.Moving()
		else:
			if self.target.position == self.Lulu.position:
				time = self.time[1]
			else:
				time = self.time[2]
			end_flag2 = self.time_count[1].Duration(time)
			if self.target.flag.condition_flag.death_flag or self.target.flag.condition_flag.miss_flag[0]:
				self.time_count[1].value = 0
				end_flag2 = True
			if end_flag2:
				# 判断终点
				self.Judg_end_point()
				# 进入移动状态
				self.moving_flag = True
				self.Lulu.champion.skill.extra[2][0][2] = True
pix = Pix()
# 战斗机
class Warcraft(object):
	def __init__(self,AurelionSol = None,game = None):
		self.AurelionSol = AurelionSol
		self.game = game
		self.num = 0												# 编号0~5
		self.flag = False                   						# 出动标志
		self.moving_flag = False									# 移动中状态
		self.time = [0.5,1] 										# 飞行时间|停留时间|移动次数
		self.step = [0,8] 											# 当前移动次数|最大移动次数
		self.time_count = [Time_count(),Time_count()]
		self.position = 0											# 母舰位置
		self.pos_num = 0
		self.orig_point = [0,0]		   								# 舱位								
		self.start_point = [0,0]					 				# 起点
		self.end_point = [0,0] 										# 终点
		self.current_point = [0,0]			 						# 当前位置	
		self.frame_number = [0,20]									# 帧数
		self.delta = [0,0]											# 每帧位移
		self.target = [None,0,0] 									# 当前目标英雄|左右侧|上中下
		self.return_flag = False 									# 回舱标志
		self.direction = 0											# 方向0朝右，1朝左

	# 舱位
	def Orig(self):
		self.orig_point[0] = 277 + 398 * self.position + 40 * self.num
		self.orig_point[1] = 203 + 230 * self.pos_num
		self.Init()
	# 初始化
	def Init(self):
		self.step[0] = 0
		self.frame_number[0] = 0
		for i in range(2):
			self.time_count[i].value = 0
		self.return_flag = False
		self.moving_flag = False
		self.delta = [0,0]
		self.target = [None,0,0]
		self.start_point[0] = self.orig_point[0]
		self.start_point[1] = self.orig_point[1]
		self.current_point[0] = self.start_point[0]
		self.current_point[1] = self.start_point[1]
		self.direction = self.position
	# 确定终点
	def Judg_end_point(self):
		# 下一个目的点的判断逻辑，非其他战斗机的目标点、左右位置互换、所在目标可选取（最多有9个选项）
		temp_target = self.target
		a = ~self.position+2
		if self.step[0] == 1:
			# 出舱随机选择左右侧
			c = randint(0,1)
		else:
			c = ~self.target[1]+2
			self.direction = ~c+2
			# 去除原占位
			warcraft_xy[a][self.target[0].pos_num][self.target[1]][self.target[2]][2] = False
		b = randint(0,2)
		d = randint(0,2)
		break_flag = False
		for _ in range(3):
			for _ in range(3):
				if (not self.game.LR[a][b].flag.condition_flag.death_flag and not self.game.LR[a][b].flag.condition_flag.miss_flag[0]) \
				and not warcraft_xy[a][b][c][d][2]:
					self.target = [self.game.LR[a][b],c,d]
					break_flag = True
					break
				else:
					d += 1
					if d == 3:
						d = 0
			if break_flag:
				break
			b += 1
			if b == 3:
				b = 0
		# 归舱
		if self.target == temp_target or self.return_flag:
			self.end_point[0] = self.orig_point[0]
			self.end_point[1] = self.orig_point[1]
			self.direction = ~self.position+2
			self.return_flag = True
		else:
			for i in range(2):
				self.end_point[i] = warcraft_xy[a][b][c][d][i]
			# 占位
			warcraft_xy[a][b][c][d][2] = True
		# 计算位移
		for i in range(2):
			self.delta[i] = int((self.end_point[i] - self.start_point[i])/self.frame_number[1])
	# 战斗机移动中
	def Moving(self):
		end_flag1 = self.time_count[0].Duration(self.time[0]/self.frame_number[1])
		if end_flag1:
			# 当前位置变化
			for i in range(2):
				self.current_point[i] += self.delta[i]
			self.frame_number[0] += 1
			if self.frame_number[0] == self.frame_number[1] or (self.delta[0] == 0 and self.delta[1] == 0):
				# 轰炸攻击
				if not self.return_flag:
					self.Attack()
				# 抵达后初始化起点
				if not self.return_flag:
					for i in range(2):
						self.start_point[i] = warcraft_xy[~self.position+2][self.target[0].pos_num][self.target[1]][self.target[2]][i]
					self.current_point[0] = self.start_point[0]
					self.current_point[1] = self.start_point[1]
					self.frame_number[0] = 0
				# 进入停留状态
				self.moving_flag = False
				# 归舱
				if self.return_flag:
					# 初始化
					self.Init()
					self.flag = False
	# 战斗机攻击，属于技能伤害且不会被格挡，不触发卢登、第一下攻击能触发爆破专家羁绊
	def Attack(self):
		temp_enemy = self.AurelionSol.enemy
		# 若目标死亡或不可选取
		if not self.target[0].flag.condition_flag.death_flag and not self.target[0].flag.condition_flag.miss_flag[0]:
			self.AurelionSol.enemy = self.target[0]
			self.AurelionSol.champion.attack_attribute.spell_attack.spell_damage = self.AurelionSol.champion.skill.para[4] * self.AurelionSol.champion.attack_attribute.spell_power
			# 伤害计算
			self.AurelionSol.Spell_attack_damage_calculation()
			# 触发爆破专家羁绊效果(仅第一次)
			if self.AurelionSol.flag.rela_flag['爆破专家'][0] and self.AurelionSol.flag.damage_calculation_flag.spell_attack and self.step[0] == 1:
				self.AurelionSol.champion.relatedness.Blast(self.AurelionSol)
			self.AurelionSol.enemy.flag.special_flag.effect['轰炸'][0] = True
			self.AurelionSol.enemy = temp_enemy
	# 战斗机主程序
	def Fly(self):
		# 移动中
		if self.moving_flag:
			self.Moving()
		else:
			if self.step[0] == 0:
				# 出舱时间很短
				time = 0.1
			else:
				time = self.time[1]
			end_flag2 = self.time_count[1].Duration(time)
			if end_flag2:
				# 上一次移动结束
				self.step[0] += 1
				if self.step[0] == self.step[1]:
					# 回舱
					self.return_flag = True
				# 判断终点
				self.Judg_end_point()
				# 进入移动状态
				self.moving_flag = True
warcraft = [Warcraft() for _ in range(6)]
for i in range(6):
	# 编号
	warcraft[i].num = i
# 提伯斯
class Tibbers(object):
	def __init__(self,Annie = None):
		self.Annie = Annie
		self.flag = False
		self.position = 0
		self.pos_num = 0
		self.normal_attack_time_count = 0
		self.attack_speed = 0.62
		self.hp_max_value = 500
		self.hp_value = self.hp_max_value
		self.shield_value = 0
		self.shield_time = 0
		self.shield_time_count = Time_count()
		self.shield_flag = False
		self.enemy = None
	# 护盾
	def Shield(self):
		time_count_flag = self.shield_time_count.Duration(self.shield_time)
		if (self.shield_value <= 0) or time_count_flag:
			# 护盾值清零
			self.shield_value = 0
			# 护盾持续时间计数值清零
			self.shield_time_count.value = 0
			self.shield_flag = False
	# 计算生命值
	def Hp(self,damage_value):
		if self.shield_value > damage_value: 	# 1：护盾值>伤害
			self.shield_value -= damage_value
		else:
			if self.shield_value > 0:						# 2：护盾值>0且<伤害
				self.hp_value -= (damage_value - self.shield_value)
				self.shield_value = 0
			else:													# 3：无护盾
				self.hp_value -= damage_value
		if self.hp_value <= 0:
			self.flag = False
	# 提伯斯普攻，能被闪避
	def Attack(self):
		# 处理护盾
		if self.shield_flag:
			self.Shield()
		self.normal_attack_time_count += 1
		if self.normal_attack_time_count >= int((1 / self.attack_speed * 100) / time_correction[0]):
			# 普攻间隔时间计数值清零
			self.normal_attack_time_count = 0
			# 敌人闪避判断
			dodge_flag = self.Annie.champion.defensive_attribute.dodge_mechanism.Dodge_judg(self.enemy) and not self.enemy.flag.condition_flag.debuff_dizz_flag \
			and not self.enemy.flag.condition_flag.debuff_frozen_flag and not self.enemy.flag.condition_flag.suppress[0]
			# 计算伤害
			self.enemy = self.Annie.enemy
			if not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
				self.Annie.champion.attack_attribute.spell_attack.spell_damage = self.Annie.champion.skill.para[1]
				if not dodge_flag:
					self.Annie.Spell_attack_damage_calculation()
					self.enemy.flag.special_flag.effect['提伯斯攻击'][0] = True
tibbers = Tibbers()
# 黑默丁格召唤的炮台
class Battery(object):
	def __init__(self,Heimerdinger = None):
		self.Heimerdinger = Heimerdinger
		self.flag = False
		self.position = 0
		self.pos_num = 0
		self.normal_attack_time_count = 0
		self.normal_attack_count = [0,3]
		self.attack_speed = 0.7
		self.time_count = [Time_count(),Time_count()] 	# 持续时间计数|普攻间隔计数
		self.enemy = None
		self.laser = [False,None] 						# 激光标志|目标
		self.super_flag = False 						# 超级炮台标志
		self.para = None
		self.first_attack = False
	# 炮台攻击：普通攻击不会被格挡但会被闪避，激光射击不会被闪避但会被格挡，炮台的第一下攻击可以触发爆破专家羁绊和卢登
	def Attack(self):
		# 持续时间判断
		exist_flag = self.Continue()
		if exist_flag:
			self.normal_attack_time_count += 1
			if self.normal_attack_time_count >= int((1 / self.attack_speed * 100) / time_correction[0]):
				# 普攻间隔时间计数值清零
				self.normal_attack_time_count = 0
				# 普攻次数计数
				self.normal_attack_count[0] += 1
				if self.normal_attack_count[0] == self.normal_attack_count[1]:
					self.normal_attack_count[0] = 0
					# 激光射击
					temp_enemy = self.enemy
					self.enemy = self.Heimerdinger.enemy
					self.laser = [True,self.enemy]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.Heimerdinger.flag.condition_flag.buff_invincible_flag and not self.Heimerdinger.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.Heimerdinger.champion.defensive_attribute.tenacity
							self.Heimerdinger.condition.dizz.Add_dizz(self.Heimerdinger,dizz_time)
					else:
						self.Heimerdinger.champion.attack_attribute.spell_attack.spell_damage = self.para[2] * self.Heimerdinger.champion.attack_attribute.spell_power
						# 计算技能伤害
						self.Heimerdinger.Spell_attack_damage_calculation()
					self.enemy = temp_enemy
				else:
					self.enemy = self.Heimerdinger.game.LR[~self.position+2][self.pos_num]
					if not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
						# 普通攻击
						# 敌人闪避判断
						dodge_flag = self.Heimerdinger.champion.defensive_attribute.dodge_mechanism.Dodge_judg(self.enemy) and not self.enemy.flag.condition_flag.debuff_dizz_flag \
						and not self.enemy.flag.condition_flag.debuff_frozen_flag and not self.enemy.flag.condition_flag.suppress[0]
						# 计算伤害
						temp_enemy = self.Heimerdinger.enemy
						self.Heimerdinger.enemy = self.enemy
						self.Heimerdinger.champion.attack_attribute.spell_attack.spell_damage = self.para[1] * self.Heimerdinger.champion.attack_attribute.spell_power
						if not dodge_flag:
							self.Heimerdinger.Spell_attack_damage_calculation()
							self.enemy.flag.special_flag.effect['炮台攻击'][0] = True
							if not self.first_attack:
								if self.Heimerdinger.flag.damage_calculation_flag.spell_attack:
									# 触发卢登回声效果
									if self.Heimerdinger.flag.weapon_flag.ldhs[0]: 
										self.Heimerdinger.flag.weapon_flag.ldhs[1] = True
										self.Heimerdinger.flag.weapon_flag.ldhs[4] = self.enemy
									# 触发爆破专家羁绊效果
									if self.Heimerdinger.flag.rela_flag['爆破专家'][0]:
										self.Heimerdinger.champion.relatedness.Blast(self.Heimerdinger)
								self.first_attack = True
						self.Heimerdinger.enemy = temp_enemy
	# 持续时间计算
	def Continue(self):
		if self.time_count[0].Duration(self.para[0]):
			self.flag = False
			return False
		else:
			return True
	# 初始化
	def Init(self):
		self.normal_attack_time_count = 0
		self.normal_attack_count[0] = 0
		self.time_count[1].value = 0
		self.laser = [False,None]
		self.first_attack = False
battery = [Battery(),Battery(),Battery()]
for i in range(3):
	battery[i].pos_num = i

# 莫德凯撒技能相关的英雄额外威胁分值
threat = {'Vayne' : 6, 'Warwick' : 4, 'Ivern' : 0, 'Skarner' : 0, 'Ashe' : 4, 'Alistar' : 0, \
'Syndra' : 15, 'Soraka' : 10, 'Renekton' : 2, 'Amumu' : 9, 'Rengar' : 20, 'Veigar' : 15, 'Varus' : 2, \
'Taric' : 9, 'Fizz' : 19, 'Nocturne' : 22, 'RekSai' : 3, 'Olaf' : 6, 'Jax' : 5, 'Nami' : 7, 'Brand' : 22, \
'Lux' : 12, 'ChoGath' : 7, 'Darius' : 3, 'Karthus' : 24, 'Thresh' : 6, 'Katarina' : 35, 'Kindred' : 11, 'Azir' : 9}

# 测试英雄
class Champion(object, metaclass = ABCMeta):
	# 参数初始化
	def __init__(self, position = 0, pos_num = 0, game = None):
		self.position = position
		self.pos_num = pos_num
		self.game = game
		self.champion = Champion_basic_parameter()					# 英雄参数
		self.enemy = None                                    		# 敌方，具体的说，这里指攻击对象
		self.friend = [None,None,None]                         		# 友方
		self.flag = Flag()											# 标志
		self.condition = Condition()								# 状态
		self.move = Move()											# 行为
		self.weapon = Weapon()										# 武器                       
	# 攻击目标判断  这里由于初始敌人是在外面给定的，所以里面只要判断更改敌人就行
	def Target_judg(self):
		result = self.game.Finish_judg()
		if result == 'Continue':
			enemy_pos_number = self.enemy.pos_num
			number = 0
			while(self.enemy.flag.condition_flag.death_flag or self.enemy.flag.condition_flag.miss_flag[0] \
				or (self.enemy.flag.special_flag.dead_area[0] and not self.flag.special_flag.dead_area[0])):
				self.enemy = self.game.LR[~self.position+2][enemy_pos_number]
				enemy_pos_number += 1 
				if enemy_pos_number > 2:
					enemy_pos_number = 0
				number += 1
				if number > 3:
					number = 0
					self.move.current_move = 'stop'
					break
			# 死者领域强制单挑
			if self.flag.special_flag.dead_area[0]:
				self.enemy = self.flag.special_flag.dead_area[1]
				if self.enemy.flag.condition_flag.miss_flag[0]:
					self.move.current_move = 'stop'
		else:
			self.move.current_move = 'stop'
	# 普攻伤害计算
	def Normal_attack_damage_calculation(self):
		# 普攻伤害计算标志清除
		self.flag.damage_calculation_flag.normal_attack = False
		# 暴击标志清除
		self.champion.attack_attribute.crit_mechanism.crit_flag = False
		# 暴击判断
		crit_flag = self.champion.attack_attribute.crit_mechanism.Crit_judg()
		if self.flag.weapon_flag.yxmr[2]:														# 触发夜袭暮刃效果
			crit_flag = True
			self.champion.attack_attribute.normal_attack.physical_damage += self.flag.weapon_flag.yxmr[3]
			self.flag.weapon_flag.yxmr[2] = False
		if self.champion.name == 'Jhin':														# 烬的第四枪必定暴击
			if self.champion.skill.para[1][0]:
				crit_flag = True
		if crit_flag and self.flag.weapon_flag.ttjj[0]:											# 触发泰坦坚决效果
			self.weapon.Ttjj(self)
		if crit_flag and self.champion.name == 'Twisted': 										# 崔斯特的卡牌攻击暴击处理
			if self.champion.skill.para[2]:
				# 显示珠光拳套触发
				if self.flag.weapon_flag.zgqt[0]:
					self.flag.weapon_flag.zgqt[3] += 1 
					self.flag.weapon_flag.zgqt[2] = True
				# 红牌AOE暴击
				if self.champion.skill.name == '红色卡牌':
					self.champion.skill.aoe[1] = True
		if crit_flag and self.flag.weapon_flag.wjzr[0]:											# 装备无尽之刃暴击时显示效果
			self.flag.weapon_flag.wjzr[2] = True
		if self.flag.weapon_flag.zyzs[0]: 														# 触发正义之手效果
			self.flag.weapon_flag.zyzs[1] = randint(1,2) 										# 1：增伤 2：回血
			if self.flag.weapon_flag.zyzs[1] == 1:												# 触发正义之手增伤效果
				self.champion.attack_attribute.normal_attack.physical_damage *= (1 + self.flag.weapon_flag.zyzs[2][0])
				self.flag.weapon_flag.zyzs[3][0] += 1
		if crit_flag and self.enemy.flag.weapon_flag.hyzw[0] and (not self.flag.weapon_flag.jshp[0]): #触发敌人幻影之舞效果
			self.enemy.flag.weapon_flag.hyzw[1] = True											# 显示触发幻影之舞
			self.enemy.flag.weapon_flag.hyzw[2] += 1
			self.enemy.champion.defensive_attribute.dodge_mechanism.dodge_count += 1
		else:
			# 触发影羁绊
			if self.flag.rela_flag['影'][0]:
				self.champion.relatedness.Shadow(self,0)
			# 暴击增幅
			if crit_flag:
				# 行动栏显示普攻暴击
				self.flag.move_flag.show_normal_attack[2] = 1
				self.champion.attack_attribute.crit_mechanism.crit_flag = True
				crit_multiple = self.champion.attack_attribute.crit_mechanism.crit_multiple
			else:
				crit_multiple = 1
			if crit_flag and self.flag.weapon_flag.ltjl[0]: 									# 触发雷霆劫掠效果
				self.weapon.Ltjl(self)
			# 普攻伤害计算
			#	物理伤害
			#	幻影之舞免疫穿甲
			if self.enemy.flag.weapon_flag.hyzw[0]:
				armor_penetration = 0
			else:
				armor_penetration = self.champion.attack_attribute.armor_penetration
			# 触发破败王者效果
			if self.flag.weapon_flag.pbwz[0]:
				self.champion.attack_attribute.normal_attack.physical_damage += (self.flag.weapon_flag.pbwz[1] * (self.enemy.champion.hp.value + self.enemy.condition.shield.value))
			self.champion.attack_attribute.normal_attack_damage.physical_damage = (self.champion.attack_attribute.normal_attack.physical_damage \
			 * (100 / (100 + (self.enemy.champion.defensive_attribute.armor * (1 - armor_penetration/100))))) * crit_multiple \
			 * self.enemy.condition.matigation.value * self.enemy.condition.iron.value
			#	魔法伤害
			if self.enemy.flag.weapon_flag.symj[1]: 											# 触发深渊面具效果
				self.enemy.flag.weapon_flag.symj[2] = 1 + self.enemy.flag.weapon_flag.symj[3]
			self.champion.attack_attribute.normal_attack_damage.spell_damage = (self.champion.attack_attribute.normal_attack.spell_damage * (100 / (100 + (self.enemy.champion.defensive_attribute.spell_resistance\
			 * ((1 - self.champion.attack_attribute.spell_resistance_penetration/100)))))) * self.enemy.flag.weapon_flag.symj[2] * crit_multiple * self.enemy.condition.matigation.value * self.enemy.condition.iron.value
			if self.enemy.flag.weapon_flag.jlzy[0]: 												# 触发敌人的巨龙之牙效果
				self.champion.attack_attribute.normal_attack_damage.spell_damage *= (1 - self.enemy.flag.weapon_flag.jlzy[1])
			# 卡萨丁贤者之石被动
			if self.enemy.champion.name == 'Kassadin':
				self.champion.attack_attribute.spell_attack_damage.spell_damage *= (1 - self.enemy.champion.skill.para[3])
			#	真实伤害
			# 触发巨人杀手效果
			if self.flag.weapon_flag.jrss[0]: 					# 触发巨人杀手效果
				self.champion.attack_attribute.normal_attack.real_damage += self.flag.weapon_flag.jrss[1] * (self.enemy.champion.hp.max_value + self.enemy.condition.shield.value)
			self.champion.attack_attribute.normal_attack_damage.real_damage = self.champion.attack_attribute.normal_attack.real_damage * crit_multiple * self.enemy.condition.iron.value
			
			# 伤害折算处理：狂战士、枪手、分裂飓风、泰坦坚决、格雷福斯中心目标、格雷福斯周围目标、忍者buff、暗影核心、奥德赛、暗星、巨九
			convert = [[(self.flag.rela_flag['狂战士'][3] and self.champion.name != 'Graves'),rela_dic['狂战士'][1][2]],[self.flag.rela_flag['枪手'][3],rela_dic['枪手'][1][2]],\
			[self.flag.weapon_flag.fljf[1],self.flag.weapon_flag.fljf[4]],[self.flag.weapon_flag.ttjj[0],self.flag.weapon_flag.ttjj[2][0]],\
			[(self.champion.name == 'Graves' and not self.flag.rela_flag['狂战士'][3] and not self.flag.rela_flag['枪手'][3]),self.champion.skill.para[0]],\
			[(self.champion.name == 'Graves' and self.flag.rela_flag['狂战士'][3] and not self.flag.rela_flag['枪手'][3]),self.champion.skill.para[1]],\
			[self.flag.rela_flag['忍者'][3],(1+rela_dic['忍者'][1][2])],[self.flag.weapon_flag.ayhx[1][0],(1+self.flag.weapon_flag.ayhx[2])],\
			[self.flag.rela_flag['奥德赛'][0],self.flag.rela_flag['奥德赛'][3]],[self.flag.rela_flag['暗星'][0],(1+self.flag.rela_flag['暗星'][1]*self.flag.rela_flag['暗星'][3])],\
			[self.flag.weapon_flag.jxjts[2],self.flag.weapon_flag.jxjts[1]]]
			for i in range(len(convert)):
				if convert[i][0]:
					self.champion.attack_attribute.normal_attack_damage.physical_damage *= convert[i][1]
					self.champion.attack_attribute.normal_attack_damage.spell_damage *= convert[i][1]
					self.champion.attack_attribute.normal_attack_damage.real_damage *= convert[i][1]

			# 触发神臂之弓效果
			if self.flag.weapon_flag.sbzg[0]:
				self.weapon.Sbzg(self,0)
			# 厄斐琉斯对影/荧焰/驻灵伤害折算
			if self.champion.name == 'Aphelios':
				if self.champion.skill.continuous[1]:
					self.Dy()
				if self.mwd_dic['荧焰'][1]:
					self.Yy()
				if self.champion.skill.para[4][2]:
					self.Zl()
			# 易双重打击
			if self.champion.name == 'Yi':
				if self.champion.skill.para[5][0]:
					self.champion.attack_attribute.normal_attack_damage.physical_damage *= self.champion.skill.para[5][1]
					self.champion.attack_attribute.normal_attack_damage.spell_damage *= self.champion.skill.para[5][1]
					self.champion.attack_attribute.normal_attack_damage.real_damage *= self.champion.skill.para[5][1]
			# 凯特琳爆头
			if self.champion.name == 'Caitlyn':
				self.champion.skill.para[3][5] = False
				if self.champion.skill.para[3][2]:
					self.champion.attack_attribute.normal_attack_damage.physical_damage *= (self.champion.skill.para[3][3] + self.champion.attack_attribute.crit_mechanism.crit_multiple)
					self.champion.attack_attribute.normal_attack_damage.spell_damage *= (self.champion.skill.para[3][3] + self.champion.attack_attribute.crit_mechanism.crit_multiple)
					self.champion.attack_attribute.normal_attack_damage.real_damage *= (self.champion.skill.para[3][3] + self.champion.attack_attribute.crit_mechanism.crit_multiple)
					self.champion.skill.para[3][2] = False
					self.champion.skill.para[3][0] = 0
					self.champion.skill.para[3][4] += 1
					self.champion.skill.para[3][5] = True

			#	总伤害
			self.champion.attack_attribute.normal_attack_damage.Total_damage_calculation()

			if not self.enemy.flag.condition_flag.buff_invincible_flag and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
				# 造成伤害
				if self.champion.attack_attribute.normal_attack_damage.total_damage > 0:
					# 触发敌人的水晶羁绊(缓和的普攻伤害可被荆棘之甲反弹)
					if self.enemy.flag.rela_flag['水晶'][0]:
						self.champion.attack_attribute.normal_attack_damage.total_damage = self.champion.relatedness.Crystal(self.enemy,self.champion.attack_attribute.normal_attack_damage.total_damage)
					# 计算扣血、判断击杀
					self.champion.hp.HP_reduce(self.champion.attack_attribute.normal_attack_damage.total_damage,self,self.enemy)
					# 计算生命偷取
					if self.champion.hemophagia > 0:
						hp_restore_value = self.champion.hemophagia * self.champion.attack_attribute.normal_attack_damage.physical_damage
						# 判断过量治疗
						if self.flag.weapon_flag.yxjj[0]:
							self.flag.special_flag.extra_heal_flag = True
						if self.champion.name == 'Aphelios':
							if self.mwd_dic['断魄'][1]:
								self.flag.special_flag.extra_heal_flag = True
						self.champion.hp.HP_restore(hp_restore_value,self.champion,self)
					# 累计造成伤害
					self.champion.attack_attribute.all_damage.Calculation(self.champion.attack_attribute.normal_attack_damage)
					
					if self.enemy.flag.weapon_flag.jjzj[0] and not self.flag.condition_flag.buff_invincible_flag: 			# 触发敌人荆棘之甲效果
						self.weapon.Jjzj(self,crit_multiple)
					if self.flag.weapon_flag.fxtx[0]:  														# 触发凡性提醒的重伤效果
						self.condition.injury.Add_injury(self.enemy, self.flag.weapon_flag.fxtx[1][1])
					elif self.flag.weapon_flag.kjqr[0]: 													# 触发科技枪刃效果
						hp_restore_value2 = self.flag.weapon_flag.kjqr[1] * self.champion.attack_attribute.normal_attack_damage.total_damage
						self.champion.hp.HP_restore(hp_restore_value2,self.champion,self)
					elif self.flag.weapon_flag.zyzs[1] == 2:												# 触发正义之手回复效果
						self.champion.hp.HP_restore(self.flag.weapon_flag.zyzs[2][1],self.champion,self)
						self.flag.weapon_flag.zyzs[3][1] += 1
					elif self.flag.weapon_flag.blsf[0]:  													# 触发卑劣手斧效果
						blsf_shield_value = int(self.champion.attack_attribute.normal_attack_damage.physical_damage/self.flag.weapon_flag.blsf[1][0])
						self.flag.weapon_flag.blsf[2] += blsf_shield_value
						self.condition.shield.Add_shield(self,blsf_shield_value,self.flag.weapon_flag.blsf[1][1])
					elif self.flag.weapon_flag.haqg[0]: 													#触发黑暗切割效果
						if self.enemy.flag.weapon_flag.haqg[2][0] < self.enemy.flag.weapon_flag.haqg[2][1] and not self.enemy.flag.weapon_flag.hyzw[0]:
							self.enemy.champion.defensive_attribute.armor *= (1 - self.enemy.flag.weapon_flag.haqg[1])
					elif self.flag.special_flag.kill[0] and self.flag.weapon_flag.lzzr[0]:					# 击杀触发领主之刃效果
				 		self.champion.attack_attribute.AD += self.flag.weapon_flag.lzzr[3][1]
				 		self.flag.weapon_flag.lzzr[1] += 1
				 		self.flag.weapon_flag.lzzr[2] = True
				 	# 普攻造成魔法伤害或真实伤害时
					if self.champion.attack_attribute.normal_attack_damage.spell_damage > 0 or self.champion.attack_attribute.normal_attack_damage.real_damage > 0:
						if self.flag.weapon_flag.swmd[0]:
							self.condition.injury.Add_injury(self.enemy, self.flag.weapon_flag.swmd[1][0])    	# 触发死亡秘典重伤效果
							self.flag.weapon_flag.swmd[2] = True
						# 显示珠光拳套触发
						if self.flag.weapon_flag.zgqt[0] and crit_flag:
							self.flag.weapon_flag.zgqt[3] += 1 
							self.flag.weapon_flag.zgqt[2] = True
					if self.flag.rela_flag['地狱火'][0]:														# 触发地狱火羁绊效果
						self.champion.relatedness.Fire(self)
					if self.flag.rela_flag['雷霆'][0]: 														# 触发雷霆羁绊
						self.champion.relatedness.Thunder(self)
					if self.flag.rela_flag['星神'][3]: 														# 触发星神羁绊
						hp_restore_value = self.flag.rela_flag['星神'][1] * self.champion.attack_attribute.normal_attack_damage.total_damage
						self.champion.hp.HP_restore(hp_restore_value,self.champion,self)
					# 普攻伤害计算标志置位
					self.flag.damage_calculation_flag.normal_attack = True
					# 凯特琳爆头充能计数
					if self.champion.name == 'Caitlyn':
						if not self.champion.skill.para[3][5]:
							if crit_flag:
								self.Headshot(2)
							else:
								self.Headshot(1)
				# 不造成伤害也能触发的攻击特效
				if self.flag.weapon_flag.cmbs[0] and not self.enemy.flag.special_flag.chakra_flag: 																			# 触发沉默匕首效果
					if randint(0,99) < 100 * self.flag.weapon_flag.cmbs[1][0]:
						self.condition.silence.Add_silence(self.enemy,self.flag.weapon_flag.cmbs[1][1])
						self.flag.weapon_flag.cmbs[2] += 1
				elif self.flag.weapon_flag.zjmd[0] and not self.enemy.flag.condition_flag.buff_unstoppable_flag: 			# 触发折戟秘刀效果
					if randint(0,99) < 100 * self.flag.weapon_flag.zjmd[1][0]:
						disarm_time = self.flag.weapon_flag.zjmd[1][1] / self.enemy.champion.defensive_attribute.tenacity
						self.condition.disarm.Add_disarm(self.enemy,disarm_time)
						self.flag.weapon_flag.zjmd[2] += 1
				# 触发极地羁绊效果
				if self.flag.rela_flag['极地'][0] and not self.enemy.flag.condition_flag.buff_unstoppable_flag and not self.enemy.flag.condition_flag.buff_invincible_flag:
					self.champion.relatedness.Ice(self)
				# 厄斐琉斯坠明的夜凝效果
				if self.champion.name == 'Aphelios':
					if self.mwd_dic['坠明'][1]:
						self.Yn()						
	# 技能伤害计算
	def Spell_attack_damage_calculation(self):
		# 技能伤害计算标志清零
		self.flag.damage_calculation_flag.spell_attack = False
		crit_flag = False
		if self.flag.weapon_flag.zgqt[0]:  									# 触发珠光拳套效果
			self.flag.weapon_flag.zgqt[1] = 1								# 法术暴击初始化
			# 暴击判断
			crit_flag = self.champion.attack_attribute.crit_mechanism.Crit_judg()
			if self.champion.skill.aoe[1]:
				crit_flag = True
			if crit_flag :
				self.flag.weapon_flag.zgqt[1] = self.champion.attack_attribute.crit_mechanism.crit_multiple
				if not self.champion.skill.aoe[1]:
					self.flag.weapon_flag.zgqt[3] += 1 
					self.flag.weapon_flag.zgqt[2] = True   					# 触发珠光拳套法术暴击时，显示到界面上
				if self.champion.skill.aoe[0]:
					self.champion.skill.aoe[1] = True						# 触发暴击时，AOE技能的中心伤害和周围伤害都暴击
		if crit_flag and self.enemy.flag.weapon_flag.hyzw[0]: 				# 触发敌人幻影之舞效果：免疫暴击
			self.enemy.flag.weapon_flag.hyzw[1] = True						# 显示触发幻影之舞
			self.enemy.flag.weapon_flag.hyzw[2] += 1
			self.enemy.champion.defensive_attribute.dodge_mechanism.dodge_count += 1
		else:
			# 触发影羁绊
			if self.flag.rela_flag['影'][0]:
				self.champion.relatedness.Shadow(self,1)
			# 物理伤害
			#	幻影之舞免疫穿甲
			if self.enemy.flag.weapon_flag.hyzw[0]:
				armor_penetration = 0
			else:
				armor_penetration = self.champion.attack_attribute.armor_penetration
			self.champion.attack_attribute.spell_attack_damage.physical_damage = (self.champion.attack_attribute.spell_attack.physical_damage * self.flag.weapon_flag.zgqt[1] \
				* (100 / (100 + (self.enemy.champion.defensive_attribute.armor * (1 - armor_penetration/100))))) * self.enemy.condition.matigation.value * self.enemy.condition.iron.value
			# 魔法伤害
			if self.enemy.flag.weapon_flag.symj[1]: 						# 触发深渊面具效果
				self.enemy.flag.weapon_flag.symj[2] = 1 + self.enemy.flag.weapon_flag.symj[3]
			self.champion.attack_attribute.spell_attack_damage.spell_damage = (self.champion.attack_attribute.spell_attack.spell_damage * self.flag.weapon_flag.zgqt[1] * (100 / (100 + (self.enemy.champion.defensive_attribute.spell_resistance\
			 * ((1 - self.champion.attack_attribute.spell_resistance_penetration/100)))))) * self.enemy.flag.weapon_flag.symj[2] * self.enemy.condition.matigation.value * self.enemy.condition.iron.value
			if self.enemy.flag.weapon_flag.jlzy[0]: 							# 触发巨龙之牙（敌人）效果
				self.champion.attack_attribute.spell_attack_damage.spell_damage *= (1 - self.enemy.flag.weapon_flag.jlzy[1])
			# 卡萨丁贤者之石被动
			if self.enemy.champion.name == 'Kassadin':
				self.champion.attack_attribute.spell_attack_damage.spell_damage *= (1 - self.enemy.champion.skill.para[3])
			# 真实伤害
			self.champion.attack_attribute.spell_attack_damage.real_damage = self.champion.attack_attribute.spell_attack.real_damage * self.flag.weapon_flag.zgqt[1] * self.enemy.condition.iron.value
			
			# 伤害折算处理：泰坦坚决、忍者buff、暗影核心、奥德赛、暗星
			convert = [[self.flag.weapon_flag.ttjj[0],self.flag.weapon_flag.ttjj[2][0]],[self.flag.rela_flag['忍者'][3],(1+rela_dic['忍者'][1][2])],\
			[self.flag.weapon_flag.ayhx[1][0],(1+self.flag.weapon_flag.ayhx[2])],[self.flag.rela_flag['奥德赛'][0],self.flag.rela_flag['奥德赛'][3]],\
			[self.flag.rela_flag['暗星'][0],(1+self.flag.rela_flag['暗星'][1]*self.flag.rela_flag['暗星'][3])]]
			for i in range(len(convert)):
				if convert[i][0]:
					self.champion.attack_attribute.spell_attack_damage.physical_damage *= convert[i][1]
					self.champion.attack_attribute.spell_attack_damage.spell_damage *= convert[i][1]
					self.champion.attack_attribute.spell_attack_damage.real_damage *= convert[i][1]

			# 触发泰坦坚决效果
			if self.flag.weapon_flag.ttjj[0]:
				self.champion.attack_attribute.spell_attack_damage.physical_damage *= self.flag.weapon_flag.ttjj[2][0]
				self.champion.attack_attribute.spell_attack_damage.spell_damage *= self.flag.weapon_flag.ttjj[2][0]
				self.champion.attack_attribute.spell_attack_damage.real_damage *= self.flag.weapon_flag.ttjj[2][0]

			# 总伤害
			self.champion.attack_attribute.spell_attack_damage.Total_damage_calculation()

			if self.champion.attack_attribute.spell_attack_damage.total_damage <= 0 or self.enemy.flag.condition_flag.buff_invincible_flag or (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
				self.champion.attack_attribute.spell_attack_damage.total_damage = 0
			else:
				# 触发敌人的水晶羁绊
				if self.enemy.flag.rela_flag['水晶'][0]:
					self.champion.attack_attribute.spell_attack_damage.total_damage = self.champion.relatedness.Crystal(self.enemy,self.champion.attack_attribute.spell_attack_damage.total_damage)
				# 扣血、判断击杀
				self.champion.hp.HP_reduce(self.champion.attack_attribute.spell_attack_damage.total_damage,self,self.enemy)
				# 累计造成伤害
				self.champion.attack_attribute.all_damage.Calculation(self.champion.attack_attribute.spell_attack_damage)
				
				if self.flag.weapon_flag.zgqt[1] != 1:
					print('%s触发珠光拳套效果，对%s造成总伤害：%d，暴击伤害：%.2f' % (self.champion.name,self.enemy.champion.name,self.champion.attack_attribute.spell_attack_damage.total_damage,self.flag.weapon_flag.zgqt[1]))
				if self.flag.weapon_flag.swmd[0] and self.champion.attack_attribute.spell_attack_damage.spell_damage > 0: 	# 触发死亡秘典的重伤效果
					self.condition.injury.Add_injury(self.enemy, self.flag.weapon_flag.swmd[1][0])
					self.flag.weapon_flag.swmd[2] = True
				if self.flag.weapon_flag.kjqr[0]: 								# 触发科技枪刃效果
					hp_restore_value3 = self.flag.weapon_flag.kjqr[1] * self.champion.attack_attribute.spell_attack_damage.total_damage
					self.champion.hp.HP_restore(hp_restore_value3,self.champion,self)
				# 触发雷霆羁绊
				if self.flag.rela_flag['雷霆'][0]:
					self.champion.relatedness.Thunder(self)
				# 触发星神羁绊
				if self.flag.rela_flag['星神'][3]: 
					hp_restore_value = self.flag.rela_flag['星神'][1] * self.champion.attack_attribute.spell_attack_damage.total_damage
					self.champion.hp.HP_restore(hp_restore_value,self.champion,self)
				# 技能伤害计算标志置位
				self.flag.damage_calculation_flag.spell_attack = True
				# 计算敌人回蓝
				self.champion.mp.MP_restore_2(self.flag, self, self.enemy, 0)
	# 普攻前特殊效果
	def Special_normal_attack(self):
		pass
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		pass
	# 普攻
	def Normal_attack(self):
		self.champion.attack_attribute.normal_attack_time_count += 1
		if self.champion.attack_attribute.normal_attack_time_count >= int((1 / self.champion.attack_attribute.attack_speed * 100) / time_correction[0]):
			# 普攻间隔时间计数值清零
			self.champion.attack_attribute.normal_attack_time_count = 0
			# 行动栏显示普攻
			if not self.flag.move_flag.show_normal_attack[0]:
				self.flag.move_flag.show_normal_attack[0] = True
				self.flag.move_flag.show_normal_attack[2] = 0
			else:
				# 刷新计时
				self.flag.move_flag.show_normal_attack[3].value = 0
				self.flag.move_flag.show_normal_attack[2] = 0
			if self.flag.weapon_flag.krdd[0]:						# 触发狂热电刀效果
				self.weapon.Krdd(self) 
			elif self.flag.weapon_flag.fljf[0]:						# 触发分裂飓风效果
				self.flag.weapon_flag.fljf[2] = True
			# 狂战士羁绊触发判断
			if self.flag.rela_flag['狂战士'][0]:
				if self.champion.name == 'Graves':
					self.flag.rela_flag['狂战士'][4] = True
				elif (randint(0,99) < int(self.flag.rela_flag['狂战士'][1] * 100)):
					self.flag.rela_flag['狂战士'][4] = True
			# 枪手羁绊触发判断
			if self.flag.rela_flag['枪手'][0]:
				if (randint(0,99) < int(self.flag.rela_flag['枪手'][1][0] * 100)):
					self.flag.rela_flag['枪手'][4] = True
			# 敌人闪避判断
			dodge_flag = self.champion.defensive_attribute.dodge_mechanism.Dodge_judg(self.enemy) and not self.enemy.flag.condition_flag.debuff_dizz_flag \
			and not self.enemy.flag.condition_flag.debuff_frozen_flag and not self.enemy.flag.condition_flag.suppress[0]
			if self.flag.weapon_flag.jshp[0]:  						# 触发疾射火炮效果(但对面闪避判断记为成功)
				dodge_flag = False
			if dodge_flag:
				# 行动栏显示普攻被闪避
				self.flag.move_flag.show_normal_attack[2] = 2
				#self.champion.attack_attribute.normal_attack_damage.total_damage = 0
				if self.enemy.flag.weapon_flag.fshf[0]: 			# 触发飞升护符效果(敌人)
					self.weapon.Fshf(self)
				elif self.enemy.flag.weapon_flag.qfzl[0]: 			# 触发清风之灵效果(敌人)
					self.weapon.Qfzl(self)
				elif self.enemy.flag.weapon_flag.bmhs[0]:			# 触发冰脉护手效果(敌人)
					self.weapon.Bmhs(self)
				elif self.flag.weapon_flag.yxmr[2]:            		# 触发夜袭暮刃效果
					self.flag.weapon_flag.yxmr[2] = False
				if self.champion.name == 'Twisted': 				# 崔斯特卡牌miss
					if self.champion.skill.para[2]:
						# 重置
						self.champion.skill.name = self.skill[0][0]
						self.champion.skill.describe = self.skill[0][1]
						self.champion.skill.para[2] = False
				elif self.champion.name == 'Caitlyn':				# 凯特琳爆头miss
					if self.champion.skill.para[3][2]:
						self.champion.skill.para[3][2] = False
						self.champion.skill.para[3][0] = 0
				elif self.champion.name == 'Volibear':				# 沃利贝尔擂首一击miss
					if self.champion.skill.para[2][0]:
						self.champion.skill.para[2][0] = False
						self.champion.skill.para[2][1] = False
			# 计算伤害
			#	普攻前特殊效果
			self.Special_normal_attack()
			#	触发日光标记
			if self.enemy.flag.special_flag.sunlight_sign[0]:
				self.champion.attack_attribute.normal_attack.spell_damage += self.enemy.flag.special_flag.sunlight_sign[1]
			#	触发皮克斯攻击
			if pix.flag and pix.target == self and self.position == pix.Lulu.position:
				pix.Attack()
			# 记录普攻伤害原值
			self.champion.attack_attribute.normal_attack_orig.physical_damage = self.champion.attack_attribute.normal_attack.physical_damage
			self.champion.attack_attribute.normal_attack_orig.spell_damage = self.champion.attack_attribute.normal_attack.spell_damage
			self.champion.attack_attribute.normal_attack_orig.real_damage = self.champion.attack_attribute.normal_attack.real_damage
			# 剑士羁绊消耗记录
			if self.flag.rela_flag['剑士'][0]:
				self.champion.relatedness.Swordsman2(self)
			if not dodge_flag:
				self.Normal_attack_damage_calculation()
				# 普攻后特殊效果
				self.Special_normal_attack2()
				# 剑士羁绊触发判定
				if self.flag.rela_flag['剑士'][0]:
					self.champion.relatedness.Swordsman1(self)
				# 巨型九头蛇效果
				if self.flag.weapon_flag.jxjts[0]:
					self.weapon.Jxjts(self)
			if self.flag.weapon_flag.gszn[0] and self.flag.damage_calculation_flag.normal_attack: 	# 触发鬼索之怒效果
				if self.champion.name == 'Jhin':
					self.As2cr(1 + self.flag.weapon_flag.gszn[1])
				else:
					self.champion.attack_attribute.attack_speed *= (1 + self.flag.weapon_flag.gszn[1])
				self.flag.weapon_flag.gszn[2] += 1
	# 技能附带攻击特效1
	def Spell_special_effect1(self):
		# 触发攻击特效1
		# 	巨人杀手
		if self.flag.weapon_flag.jrss[0]:
			self.champion.attack_attribute.spell_attack.real_damage += self.flag.weapon_flag.jrss[1] * (self.enemy.champion.hp.max_value + self.condition.shield.value)
		# 	正义之手
		if self.flag.weapon_flag.zyzs[0]:
			self.flag.weapon_flag.zyzs[1] = randint(1,2) 	# 1：增伤 2：回血
			if self.flag.weapon_flag.zyzs[1] == 1:			# 触发正义之手增伤效果	
				self.champion.attack_attribute.spell_attack_damage.physical_damage *= (1 + self.flag.weapon_flag.zyzs[2][0])
				self.flag.weapon_flag.zyzs[3][0] += 1
		# 	神臂之弓
		if self.flag.weapon_flag.sbzg[0]:
			self.weapon.Sbzg(self,1)
	# 技能附带攻击特效2
	def Spell_special_effect2(self):
		# 触发攻击特效2
		if self.flag.damage_calculation_flag.spell_attack:
			#	朔极之矛
			if self.flag.weapon_flag.sjzm[1]:    
				self.champion.mp.Calculation(self,int(self.flag.weapon_flag.sjzm[2] * self.champion.mp.max_value))
			#	生命偷取
			if self.champion.hemophagia > 0:													
				hp_restore_value = self.champion.hemophagia * self.champion.attack_attribute.spell_attack_damage.physical_damage
				# 判断过量治疗
				if self.flag.weapon_flag.yxjj[0]:
					self.flag.special_flag.extra_heal_flag = True
				if self.champion.name == 'Aphelios':
					if self.mwd_dic['断魄'][1]:
						self.flag.special_flag.extra_heal_flag = True
				self.champion.hp.HP_restore(hp_restore_value,self.champion,self)
			#	卑劣手斧
			if self.flag.weapon_flag.blsf[0]: 
				self.condition.shield.Add_shield(self,int(self.champion.attack_attribute.spell_attack_damage.physical_damage/self.flag.weapon_flag.blsf[1][0]),self.flag.weapon_flag.blsf[1][1])
			#	鬼索之怒
			if self.flag.weapon_flag.gszn[0]:
				self.champion.attack_attribute.attack_speed *= (1 + self.flag.weapon_flag.gszn[1])
				self.flag.weapon_flag.gszn[2] += 1
			#	凡性提醒
			if self.flag.weapon_flag.fxtx[0] and not self.enemy.flag.condition_flag.buff_invincible_flag and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
				self.condition.injury.Add_injury(self.enemy, self.flag.weapon_flag.fxtx[1][1])
			# 	正义之手回血效果
			if self.flag.weapon_flag.zyzs[0] and self.flag.weapon_flag.zyzs[1] == 2:
				self.champion.hp.HP_restore(self.flag.weapon_flag.zyzs[2][1],self.champion,self)
				self.flag.weapon_flag.zyzs[3][1] += 1
			# 地狱火羁绊
			if self.flag.rela_flag['地狱火'][0]:
				self.champion.relatedness.Fire(self)
		# 不造成伤害也可以触发的攻击特效
		#	沉默匕首
		if self.flag.weapon_flag.cmbs[0] and not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.special_flag.chakra_flag and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
			if randint(0,99) < 100 * self.flag.weapon_flag.cmbs[1][0]:
				self.condition.silence.Add_silence(self.enemy,self.flag.weapon_flag.cmbs[1][1])
				self.flag.weapon_flag.cmbs[2] += 1
		#	折戟秘刀
		if self.flag.weapon_flag.zjmd[0] and not self.enemy.flag.condition_flag.buff_unstoppable_flag and not self.enemy.flag.condition_flag.buff_invincible_flag and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]): 													
			if randint(0,99) < 100 * self.flag.weapon_flag.zjmd[1][0]:
				disarm_time = self.flag.weapon_flag.zjmd[1][1] / self.enemy.champion.defensive_attribute.tenacity
				self.condition.disarm.Add_disarm(self.enemy,disarm_time)
				self.flag.weapon_flag.zjmd[2] += 1
		# 	极地羁绊
		if self.flag.rela_flag['极地'][0] and not self.enemy.flag.condition_flag.buff_unstoppable_flag and not self.enemy.flag.condition_flag.buff_invincible_flag: 
			self.champion.relatedness.Ice(self)
		# 厄斐琉斯坠明的夜凝效果
		if self.champion.name == 'Aphelios':
			if self.mwd_dic['坠明'][1]:
				self.Yn()
	# 施法后特殊效果
	def Special_spell_attack(self):
		# 触发朔极之矛效果
		if self.flag.weapon_flag.sjzm[0] and not self.flag.weapon_flag.sjzm[1] and not self.flag.special_flag.chakra_flag:
			self.flag.weapon_flag.sjzm[1] = True
		# 触发夜袭暮刃效果
		if self.flag.weapon_flag.yxmr[0] and not self.flag.weapon_flag.yxmr[2]:
			self.flag.weapon_flag.yxmr[2] = True
	# 使用技能（施法）
	@abstractmethod
	def Spell_attack(self):
		pass
	# 技能特殊效果处理
	def Special_effect_deal(self):
		pass
	# 技能特殊效果处理2：与死亡状态无关—
	def Special_effect_deal2(self):
		pass
	# 通用击杀效果处理
	def Kill_deal1(self):
		# 触发樱手里剑效果
		if self.flag.weapon_flag.yslj[0]:
			chakra = self.flag.special_flag.kill[4] * self.flag.weapon_flag.yslj[2] * self.champion.mp.max_value
			self.champion.mp.Calculation(self,chakra)
			self.flag.weapon_flag.yslj[4] += self.flag.special_flag.kill[4]
			self.flag.weapon_flag.yslj[3] = True
		# 刷新暗影核心效果
		if self.flag.weapon_flag.ayhx[0]:
			self.flag.weapon_flag.ayhx[1][0] = True
			self.flag.weapon_flag.ayhx[1][1].value = 0
		# 技能击杀效果
		self.Kill_deal()
	# 专有击杀效果处理
	def Kill_deal(self):
		pass
	# 死亡处理
	def Death_deal(self):
		# 光羁绊效果
		self.champion.relatedness.Light(self)
		if not self.champion.name == 'VoidMonster':
			# 暗星羁绊效果
			self.champion.relatedness.Death(self)
		# 孤立无援标记清除
		self.flag.special_flag.ooal_sign = False
		# 触发太阳圆盘
		if self.game.desert_flag[self.position][0] and not self.game.desert_flag[self.position][1] and not self.flag.special_flag.dead_area[0]\
		and not self.game.SolarDisk[0]:
			for i in range(3):
				if self.friend[i].champion.name == 'Azir' and not self.friend[i].flag.condition_flag.death_flag:
					self.game.SolarDisk[0] = True
					self.game.SolarDisk[3] = self
					self.game.SolarDisk[4] = self.friend[i]
					self.game.desert_flag[self.position][1] = True
		#其他特殊死亡处理
		self.Death_deal_other()
	#	其他特殊死亡处理(如魔腾)
	def Death_deal_other(self):
		pass
	# 羁绊/武器效果处理1
	def R_w_effect_deal1(self):
		# 处理神圣救赎、基克先驱、冰霜之心、深渊面具、暗影核心、淬炼勋章、银月羁绊、海洋羁绊、未来战士羁绊
		if self.flag.weapon_flag.ssjs[4][0]:
			self.weapon.Ssjs(self)
		elif self.flag.weapon_flag.jkxq[0]:
			self.weapon.Jkxq(self)
		elif self.flag.weapon_flag.bszx[0]:
			self.weapon.Bszx(self)
		elif self.flag.weapon_flag.symj[0]:
			self.weapon.Symj(self)
		elif self.flag.weapon_flag.ayhx[0]:
			self.weapon.Ayhx(self)
		elif self.flag.weapon_flag.clxz[4]:
			if self.flag.weapon_flag.clxz[5][0].Duration(self.flag.weapon_flag.clxz[5][1]):
				self.flag.weapon_flag.clxz[4] = False
		if self.game.moon_flag[self.position][0]:
			self.champion.relatedness.Moon(self.game,self.position)
		if self.game.sea_flag[self.position][0]:
			self.champion.relatedness.Sea(self.game,self.position)
		if self.game.future_flag[self.position][0]:
			self.champion.relatedness.Future(self.game,self.position)
	# 羁绊/武器效果处理2
	def R_w_effect_deal2(self):
		if not self.flag.condition_flag.miss_flag[0]:
			# 森林羁绊效果处理
			if self.flag.rela_flag['森林'][0]:
				self.champion.relatedness.Forest(self)
			# 狂徒铠甲效果处理
			if self.flag.weapon_flag.ktkj[0]:
				self.weapon.Ktjk(self)
		# 斑比熔渣效果处理
		if self.flag.weapon_flag.bbrz[0]:
			self.weapon.Bbrz(self)
		# 游侠羁绊效果处理
		if self.flag.rela_flag['游侠'][0]:
			self.champion.relatedness.Ranger(self)
		# 夜之锋刃效果处理
		if self.flag.weapon_flag.yzfr[0]:
			self.weapon.Yzfr(self)
	# 第二件武器判断
	def Second_weapon_judg(self):
		if (self.champion.hp.value <= (0.75 * self.champion.hp.max_value)) and (not self.flag.special_flag.get_weapon_flag[1]) and not self.champion.name in ('SolarDisk','VoidMonster'):
			if self.champion.name in ('Garen','SuperGaren'):
				self.weapon.weapon[1] = '巨人腰带'
			else:
				self.weapon.weapon[1] = '钢铁锁甲'
				self.weapon.weapon[1] = basic_weapon.get(randint(1, 9))
			self.weapon.Equip_weapon(2,self)
			self.flag.special_flag.get_weapon_flag[1] = True  
	# 攻击
	def Attack(self): 
		self.R_w_effect_deal1()
		self.Special_effect_deal2()
		if self.flag.condition_flag.death_flag:
			if not self.flag.special_flag.death_deal:
				self.Death_deal()
				self.flag.special_flag.death_deal = True
		else:
			# 开局获得第一件武器
			if not self.flag.special_flag.get_weapon_flag[0] and not self.champion.name in ('SolarDisk','VoidMonster'):
				if self.champion.name in ('Garen','SuperGaren'):
					self.weapon.weapon[0] = '反曲之弓'
				else:
					self.weapon.weapon[0] = '暴风大剑'
					self.weapon.weapon[0] = basic_weapon.get(randint(1, 9))    	# 开局随机获得第1件武器
				self.weapon.Equip_weapon(1,self)
				self.flag.special_flag.get_weapon_flag[0] = True
			# 造成伤害标志初始化
			self.flag.damage_calculation_flag.__init__()
			# 普攻及技能伤害初始化
			self.champion.attack_attribute.normal_attack.__init__(self.champion.attack_attribute.AD)
			self.champion.attack_attribute.spell_attack.__init__()
			# 造成击杀初始化
			self.flag.special_flag.kill = [False,None,None,None,0]
			# 判断血量，若血量低于75%最大生命值，则获得第二件基础装备
			self.Second_weapon_judg()
			# 状态处理
			self.condition.Condition_deal(self.flag,self)
			# 特殊效果处理
			self.Special_effect_deal()
			self.R_w_effect_deal2()
			# 施法判断
			if self.champion.skill.active_skill:
				self.move.Cast_spell_judg(self)
			# 攻击目标判断
			self.Target_judg()
			# 行为判断
			self.move.Move_judg(self)
			# 普攻行为，进行普攻
			if self.flag.move_flag.normal_attack:
				self.Normal_attack()
				# 普攻后计算回蓝
				self.champion.mp.MP_restore_1(self.flag, self, self.enemy)
			# 分裂飓风效果处理
			if self.flag.weapon_flag.fljf[2]: 			# 触发分裂飓风效果
				self.weapon.Fljf(self)
			# 狂战士羁绊效果处理
			if self.flag.rela_flag['狂战士'][4]:
				self.champion.relatedness.Berserker(self)
			# 枪手羁绊效果处理
			if self.flag.rela_flag['枪手'][4]:
				self.champion.relatedness.Marksman(self)
			# 施法行为，技能攻击，考虑普攻时可能被反甲反死
			if self.flag.move_flag.cast_spell and (not self.flag.condition_flag.death_flag) and (not self.flag.condition_flag.miss_flag[0]) :
				if not self.flag.condition_flag.buff_invincible_flag and not self.champion.skill.continuous[1] and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):  	# 触发离子火花效果
					if self.champion.skill.comb[0]: # 两段技能只触发一次离子火花
						if self.champion.skill.comb[1] == 0:
							self.weapon.Lzhh(self)
					else:
						self.weapon.Lzhh(self)
				if (not self.flag.condition_flag.death_flag) and (not self.flag.condition_flag.miss_flag[0]):
					# 蓝量清零
					self.champion.mp.value = 0
					self.Spell_attack()
					# 施法后清除破法状态
					if self.flag.condition_flag.debuff_broken_flag:
						self.condition.broken.Clean(self)
					# 施法结束时重置普攻(金克丝切枪不重置普攻)
					if not self.champion.name == 'Jinx':
						self.champion.attack_attribute.normal_attack_time_count = 0
					if ((self.flag.weapon_flag.tszy[0] and not self.champion.skill.comb[0]) or (self.flag.weapon_flag.tszy[0] and self.champion.skill.comb[0] and self.champion.skill.comb[1] == 0))\
					and not self.flag.special_flag.chakra_flag:  	
						self.flag.weapon_flag.tszy[1] = True 	# 触发天使之拥效果
						self.champion.mp.Calculation(self,self.flag.weapon_flag.tszy[2])
					elif self.flag.weapon_flag.clxz[0] and not self.flag.weapon_flag.clxz[4]:
						self.flag.weapon_flag.clxz[3] = True
						self.condition.shield.Add_shield(self,self.flag.weapon_flag.clxz[1]*self.champion.hp.max_value,self.flag.weapon_flag.clxz[2])
						self.flag.weapon_flag.clxz[4] = True
			if self.flag.weapon_flag.ldhs[1]:			# 触发卢登回声效果
				self.flag.weapon_flag.ldhs[2] = True 	# 显示触发卢登回声
				self.weapon.Ldhs(self,self.flag.weapon_flag.ldhs[4])
			# 击杀效果处理
			if self.flag.special_flag.kill[0]:
				self.Kill_deal1()
			# 判断造成伤害标志
			self.flag.damage_calculation_flag.Total_damage_judg()

# 01薇恩
class Vayne(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 1
		self.champion.name = 'Vayne'
		self.champion.skill.name = '圣银弩箭'
		self.champion.skill.describe = ['圣银弩箭：薇恩每第3次攻击造成基于','(目标最大生命值+护盾值)10%的额外','真实伤害(受法强加成)']
		self.champion.skill.active_skill = False
		self.champion.hp.max_value = 830
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 0
		self.champion.mp.max_value = 0
		self.champion.attack_attribute.attack_speed = 0.71
		self.champion.attack_attribute.AD = 46
		self.champion.defensive_attribute.armor = 26
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '光'
		self.champion.relatedness.profession[0] = '游侠'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['终极时刻',['终极时刻：当薇恩生命值低于25%时，','获得额外40点AD和35%闪避率，持续5s，','期间击杀敌人可延长3s持续时间'],False]
		self.champion.skill.para = [0.1,[0.25,[40,0.35],5,3,Time_count(),False]]
	
	def Spell_attack(self):
		pass
	# 普攻前特殊效果
	def Special_normal_attack(self):
		# 计算额外真实伤害
		self.champion.attack_attribute.attack_count += 1
		if self.champion.attack_attribute.attack_count == 3:
			self.flag.move_flag.show_cast_spell[0] = True
			self.champion.attack_attribute.normal_attack.real_damage = self.champion.skill.para[0] * (self.enemy.champion.hp.max_value + \
				self.enemy.condition.shield.value) * self.champion.attack_attribute.spell_power
			self.champion.attack_attribute.attack_count = 0
		else:
			self.champion.attack_attribute.normal_attack.real_damage = 0
	# 终极时刻
	def Ultimate(self):
		self.champion.skill.extra[2][0][2] = True
		self.champion.skill.para[1][5] = True
		self.champion.attack_attribute.AD += self.champion.skill.para[1][1][0]
		self.champion.defensive_attribute.dodge_mechanism.Add_dodge(self.champion.skill.para[1][1][1])
	# 终极时刻结束处理
	def Special_effect_deal(self):
		if self.champion.skill.extra[2][0][2]:
			end_flag = self.champion.skill.para[1][4].Duration(self.champion.skill.para[1][2])
			if end_flag:
				self.champion.attack_attribute.AD -= self.champion.skill.para[1][1][0]
				self.champion.defensive_attribute.dodge_mechanism.Add_dodge(-self.champion.skill.para[1][1][1])
				self.champion.skill.extra[2][0][2] = False
	# 击杀效果
	def Kill_deal(self):
		if self.champion.skill.extra[2][0][2]:
			self.champion.skill.para[1][2] += self.champion.skill.para[1][3]
# 02沃里克
class Warwick(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 2
		self.champion.name = 'Warwick'
		if version[0] == 1:
			self.champion.skill.name = '野兽之口'
			self.champion.skill.describe = ['野兽之口：沃里克撕咬目标，造成','(1.3*AD)加目标15%最大生命值的魔法','伤害，获得80%实际伤害值的治疗效果']
			self.champion.skill.para = [1.3,0.15,0.8]
			self.champion.mp.value = 40
			self.champion.mp.max_value = 100
		elif version[0] == 2:
			self.champion.skill.name = '无尽束缚'
			self.champion.skill.describe = ['无尽束缚：沃里克跃向敌人，对敌人','造成60点魔法伤害并压制1.6s，期间','获得100%生命偷取并进行4次追加普攻']
			self.champion.skill.para = [60,[Time_count(),0.4],1.6,[0,4],1.0,None]
			# 持续施法技能
			self.champion.skill.continuous[0] = True
			self.champion.mp.value = 40
			self.champion.mp.max_value = 130
		self.champion.hp.max_value = 940
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.attack_attribute.attack_speed = 0.63
		self.champion.attack_attribute.AD = 44
		self.champion.defensive_attribute.armor = 30
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '极地'
		self.champion.relatedness.profession[0] = '掠食者'

	# 使用技能（施法）
	def Spell_attack(self):
		if self.champion.skill.name == '野兽之口':
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] * self.champion.attack_attribute.AD \
					+ self.champion.skill.para[1] * self.enemy.champion.hp.max_value )* self.champion.attack_attribute.spell_power
				# 伤害计算
				self.Spell_attack_damage_calculation()
				# 获得治疗
				value_treatment = self.champion.skill.para[2] * self.champion.attack_attribute.spell_attack_damage.total_damage
				self.champion.hp.HP_restore(value_treatment,self.champion,self)
				if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
					self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
					self.flag.weapon_flag.crxl[3] = True
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
			# 行为标志处理
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.cast_spell = False
			self.Special_spell_attack()
			self.move.current_move = 'normal_attack'
		elif self.champion.skill.name == '无尽束缚':
			# 开始施法
			if not self.champion.skill.continuous[1]:
				self.champion.skill.continuous[1] = True
				self.flag.move_flag.show_cast_spell[0] = True
				self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[2]
				self.champion.skill.para[5] = self.enemy
				self.Special_spell_attack()
				# 不可阻挡状态
				self.condition.unstoppable.Add_unstoppable(self,self.champion.skill.para[2])
				# 压制敌人
				if not self.enemy.flag.condition_flag.buff_invincible_flag:
					self.enemy.condition.suppress.Add_suppress(self.enemy)
					self.flag.condition_flag.suppress[1] = True
					# 造成技能伤害
					# 	处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
						# 伤害计算
						self.Spell_attack_damage_calculation()
						# 触发卢登
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack:
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
					# 获得额外生命偷取
					self.champion.hemophagia += self.champion.skill.para[4]
					if self.flag.weapon_flag.sjzm[0] and (not self.flag.weapon_flag.sjzm[1]):			# 触发朔极之矛效果
						self.flag.weapon_flag.sjzm[1] = True
					if self.flag.weapon_flag.yxmr[0] and not self.flag.weapon_flag.yxmr[2]:             # 触发夜袭暮刃效果
						self.flag.weapon_flag.yxmr[2] = True
				# 若目标处于无敌状态则施法失败，进入CD，但会回复少量蓝量
				else:
					self.champion.skill.continuous[3] = True
					self.condition.unstoppable.Clean(self.flag)
					print('目标%s处于无敌状态，沃里克施法失败，回复20点蓝量' % self.enemy.champion.name)
					self.champion.mp.Calculation(self,20)
					self.champion.skill.para[5] = None
					self.champion.skill.continuous[1] = False
			# 施法中
			if self.champion.skill.continuous[1]:
				#	目标死亡或无法选取则中断施法
				if self.champion.skill.para[5].flag.condition_flag.death_flag or self.champion.skill.para[5].flag.condition_flag.miss_flag[0]:
					self.champion.skill.para[1][0].value = 0
					self.champion.skill.continuous[3] = True
					self.condition.unstoppable.Clean(self.flag)
					print('沃里克持续施法期间目标%s死亡或不可选取，中断施法' %(self.champion.skill.para[5].champion.name))
				else:
					end_flag = self.champion.skill.para[1][0].Duration(self.champion.skill.para[1][1])
					# 施法结束
					if end_flag:
						# 普攻计数溢出
						self.champion.attack_attribute.normal_attack_time_count = 1000
						# 普攻伤害初始化
						self.champion.attack_attribute.normal_attack.__init__(self.champion.attack_attribute.AD)
						# 追加普攻
						self.Normal_attack()
						# 计算回蓝
						self.champion.mp.MP_restore_1(self.flag, self, self.enemy)
						# 三段追加普攻计数
						self.champion.skill.para[3][0] += 1
			if self.champion.skill.para[3][0] >= self.champion.skill.para[3][1] or self.champion.skill.continuous[3]:
				self.champion.skill.para[3][0] = 0
				# 解除压制
				self.flag.condition_flag.suppress[1] = False
				self.enemy.condition.suppress.Clean(self.enemy)
				self.champion.skill.para[5] = None
				# 回复生命偷取
				self.champion.hemophagia -= self.champion.skill.para[4]
				self.champion.skill.continuous[1] = False
				self.champion.skill.continuous[2] = True
				# 行为标志处理
				self.flag.move_flag.cast_spell = False
				self.move.current_move = 'normal_attack'
	# 死亡或进入不可选取状态时解除压制
	def Special_effect_deal2(self):
		if version[0] == 2:
			if self.champion.skill.para[5] != None and (self.flag.condition_flag.death_flag or self.flag.condition_flag.miss_flag[0]):
				# 解除压制
				self.enemy.condition.suppress.Clean(self.enemy)
				self.champion.skill.para[5] = None
# 03艾翁
class Ivern(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 3
		self.champion.name = 'Ivern'
		self.champion.skill.name = '种豆得瓜'
		self.champion.skill.describe = ['种豆得瓜：艾翁为友方生命值最低的','英雄提供210点护盾，持续5s']
		self.champion.hp.max_value = 920
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 70
		self.champion.mp.max_value = 90
		self.champion.attack_attribute.attack_speed = 0.63
		self.champion.attack_attribute.AD = 41
		self.champion.defensive_attribute.armor = 38
		self.champion.defensive_attribute.spell_resistance = 29
		self.champion.relatedness.element[0] = '森林'
		self.champion.relatedness.profession[0] = '秘术师'
		self.champion.skill.para = [210,5]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		hp_min = self.champion.hp.value + self.condition.shield.value
		friend_pos_number = 0
		for i in range(3):
			if (not self.friend[i].flag.condition_flag.death_flag) and (not self.friend[i].flag.condition_flag.miss_flag[0]) \
			and not (self.friend[i].flag.special_flag.dead_area[0] and not self.flag.special_flag.dead_area[0])\
			and (self.friend[i].champion.hp.value + self.friend[i].condition.shield.value) <= hp_min:
				hp_min = self.friend[i].champion.hp.value + self.friend[i].condition.shield.value
				friend_pos_number = i
		if not self.flag.special_flag.dead_area[0]:
			target = self.friend[friend_pos_number]
		else:
			target = self
		# 获得护盾
		shield_add = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
		self.condition.shield.Add_shield(target,shield_add,self.champion.skill.para[1])
		if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
			self.condition.fervor.Add_fervor(target,self.flag.weapon_flag.crxl[2][2])
			self.flag.weapon_flag.crxl[3] = True	
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 04斯卡纳
class Skarner(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 4
		self.champion.name = 'Skarner'
		self.champion.skill.name = '水晶蝎甲'
		self.champion.skill.describe = ['水晶蝎甲：斯卡纳全身覆盖水晶，获','得170点护盾(受法强加成)，持续4s']
		self.champion.hp.max_value = 990
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 0
		self.champion.mp.max_value = 95
		self.champion.attack_attribute.attack_speed = 0.63
		self.champion.attack_attribute.AD = 48
		self.champion.defensive_attribute.armor = 44
		self.champion.defensive_attribute.spell_resistance = 24
		self.champion.relatedness.element[0] = '水晶'
		self.champion.relatedness.profession[0] = '掠食者'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['水晶之力',['水晶之力：当存在护盾时，斯卡纳提','升40%攻击速度'],False]

		self.champion.skill.para = [170,4,0.4,False]

	# 使用技能（施法）
	def Spell_attack(self):
		# 获得护盾
		shield_add = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
		self.condition.shield.Add_shield(self,shield_add,self.champion.skill.para[1])
		if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
			self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
			self.flag.weapon_flag.crxl[3] = True
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 水晶之力
	def Special_effect_deal(self):
		if self.flag.condition_flag.buff_shield_flag and not self.champion.skill.para[3]:
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[2])
				self.champion.skill.para[3] = True
				self.champion.skill.extra[2][0][2] = True
		elif (not self.flag.condition_flag.buff_shield_flag) and self.champion.skill.para[3]:
			# 攻速回到原样
			self.champion.attack_attribute.attack_speed /= (1 + self.champion.skill.para[2])
			# 标志重置
			self.champion.skill.para[3] = False
			self.champion.skill.extra[2][0][2] = False		
# 05艾希
class Ashe(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 5
		self.champion.name = 'Ashe'
		self.champion.skill.name = '魔法水晶箭'
		self.champion.skill.describe = ['魔法水晶箭：艾希向敌人发射魔法水','晶箭，对敌人造成170点魔法伤害并使','敌人冰冻5s']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 160
		self.champion.attack_attribute.attack_speed = 0.72
		self.champion.attack_attribute.AD = 50
		self.champion.defensive_attribute.armor = 30
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '极地'
		self.champion.relatedness.profession[0] = '游侠'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['冰霜射击',['冰霜射击：攻击冰冻目标时，物理伤','害增幅(50%+50%*暴击伤害倍数)','触发次数：0'],False]

		self.champion.skill.para = [170,5,[0.5,0.5,0]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			# 伤害计算
			self.Spell_attack_damage_calculation()
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
				# 冰冻效果处理
				frozen_time = self.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
				if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
					frozen_time += self.flag.weapon_flag.jdzc[1]
					self.flag.weapon_flag.jdzc[2] = True
					self.flag.weapon_flag.jdzc[3] += 1
				if self.enemy.flag.condition_flag.debuff_burn_flag:
					self.enemy.condition.burn.Clean(self.enemy.flag)
					print('冰消火')
				self.enemy.condition.frozen.Add_frozen(self.enemy,frozen_time)
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 普攻前特殊效果：冰霜射击
	def Special_normal_attack(self):
		if self.enemy.flag.condition_flag.debuff_frozen_flag:
			self.champion.skill.para[2][2] += 1
			self.champion.skill.extra[2][0][2] = True
			# 物理伤害增幅
			amplification = self.champion.skill.para[2][0] + self.champion.skill.para[2][1] * self.champion.attack_attribute.crit_mechanism.crit_multiple
			self.champion.attack_attribute.normal_attack.physical_damage *= amplification
# 06阿利斯塔
class Alistar(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 6
		self.champion.name = 'Alistar'
		self.champion.skill.name = '坚定意志'
		self.champion.skill.describe = ['坚定意志：阿利斯塔移除身上所有的','控制效果，增加20%韧性，并得到70%','减伤(持续7s)']
		self.champion.hp.max_value = 1200
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 60
		self.champion.mp.max_value = 180
		self.champion.attack_attribute.attack_speed = 0.57
		self.champion.attack_attribute.AD = 42
		self.champion.defensive_attribute.armor = 45
		self.champion.defensive_attribute.spell_resistance = 35
		self.champion.relatedness.element[0] = '钢铁'
		self.champion.relatedness.profession[0] = '守护神'
		self.flag.special_flag.force_spell = True # 可强制施法
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['野蛮怒吼',['野蛮怒吼：阿利斯塔在坚定意志期间','能吸引刺客将技能目标选为阿利斯塔'],False]

		self.champion.skill.para = [0.2,0.7,7,False]
	
	# 使用技能（施法）
	def Spell_attack(self):
		# 移除所有控制效果(眩晕、缴械、冰冻)
		self.condition.dizz.Clean(self.flag,self)
		self.condition.frozen.Clean(self.flag,self)
		self.condition.disarm.Clean(self.flag,self)
		# 增加韧性
		self.champion.defensive_attribute.Add_tenacity(self.champion.skill.para[0])
		# 减伤效果
		matigation_value = 1 - self.champion.skill.para[1]
		self.condition.matigation.Add_matigation(self,matigation_value,self.champion.skill.para[2])
		self.champion.skill.para[3] = True

		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'

	# 技能被动效果(技能特殊效果处理)
	def Special_effect_deal(self):
		# 阿利斯塔吸引刺客效果
		if self.flag.condition_flag.buff_matigation_flag:
			self.champion.skill.para[3] = True
			self.champion.skill.extra[2][0][2] = True
		else:
			self.champion.skill.para[3] = False
			self.champion.skill.extra[2][0][2] = False
# 07辛德拉
class Syndra(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 7
		self.champion.name = 'Syndra'
		self.champion.skill.name = '水力法球'
		self.champion.skill.describe = ['水力法球：辛德拉施放水力法球，对','目标造成120点魔法伤害，并对目标周','围的敌人造成90点魔法伤害']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 32
		self.champion.defensive_attribute.armor = 30
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '海洋'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['卓尔不凡',['卓尔不凡：辛德拉每次施法后提升下','次技能15%魔法伤害','层数：0'],False]

		self.champion.skill.para = [120,90,0.15,0]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * math.pow((1 + self.champion.skill.para[2]), self.champion.skill.para[3]) * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
		if not self.flag.special_flag.dead_area[0]:
			# 周围伤害计算
			temp_enemy = self.enemy
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * math.pow((1 + self.champion.skill.para[2]), self.champion.skill.para[3]) * self.champion.attack_attribute.spell_power
			temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
				and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.special_flag.dead_area[0]):
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					else:
						self.Spell_attack_damage_calculation()
			self.enemy = temp_enemy
			self.champion.skill.aoe[1] = False
		# 卓尔不凡效果
		self.champion.skill.extra[2][0][2] = True
		self.champion.skill.para[3] += 1
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 08索拉卡
class Soraka(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 8
		self.champion.name = 'Soraka'
		self.champion.skill.name = '祈愿'
		self.champion.skill.describe = ['祈愿：索拉卡祈愿，为每个(活着的)','队友回复120点生命值，且对生命值低','于30%的队友造成130%的回复效果']
		self.champion.hp.max_value = 800
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 150
		self.champion.attack_attribute.attack_speed = 0.66
		self.champion.attack_attribute.AD = 35
		self.champion.defensive_attribute.armor = 20
		self.champion.defensive_attribute.spell_resistance = 23
		self.champion.relatedness.element[0] = '光' if version[0] == 1 else '星之守护者'
		self.champion.relatedness.profession[0] = '秘术师'

		self.champion.skill.para = [120,0.3,1.3]
	# 使用技能（施法）
	def Spell_attack(self):
		# 回复生命值
		if not self.flag.special_flag.dead_area[0]:
			for i in range(3):
				if (not self.friend[i].flag.condition_flag.death_flag) and (not self.friend[i].flag.condition_flag.miss_flag[0]) and (not self.friend[i].flag.special_flag.dead_area[0]):
					if self.friend[i].champion.hp.value <= self.champion.skill.para[1] * self.friend[i].champion.hp.max_value:
						self.friend[i].champion.hp.HP_restore(self.champion.skill.para[0]*self.champion.skill.para[2]*self.champion.attack_attribute.spell_power, self.champion, self.friend[i])
						if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
							self.condition.fervor.Add_fervor(self.friend[i],self.flag.weapon_flag.crxl[2][2])
							self.flag.weapon_flag.crxl[3] = True
						self.friend[i].flag.special_flag.effect[self.champion.skill.name][0] = True
					else:
						self.friend[i].champion.hp.HP_restore(self.champion.skill.para[0]*self.champion.attack_attribute.spell_power, self.champion, self.friend[i])
						if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
							self.condition.fervor.Add_fervor(self.friend[i],self.flag.weapon_flag.crxl[2][2])
							self.flag.weapon_flag.crxl[3] = True
						self.friend[i].flag.special_flag.effect[self.champion.skill.name][0] = True
		else:
			self.champion.hp.HP_restore(self.champion.skill.para[0]*self.champion.skill.para[2]*self.champion.attack_attribute.spell_power, self.champion, self)
			if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
				self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
				self.flag.weapon_flag.crxl[3] = True
			self.flag.special_flag.effect[self.champion.skill.name][0] = True
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 09雷克顿
class Renekton(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 9
		self.champion.name = 'Renekton'
		self.champion.skill.name = '冷酷捕猎'
		self.champion.skill.describe = ['冷酷捕猎：雷克顿挥舞战刃并破坏敌','人的护盾，然后造成85点魔法伤害以','及1.4*AD的物理伤害，并使敌人眩晕','2s(破盾时则为5s)']
		self.champion.hp.max_value = 960
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 100
		self.champion.attack_attribute.attack_speed = 0.63
		self.champion.attack_attribute.AD = 50
		self.champion.defensive_attribute.armor = 38
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '沙漠'
		self.champion.relatedness.profession[0] = '狂战士'

		self.champion.skill.para = [85,1.4,[False,2,5]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			# 先破盾
			if self.enemy.condition.shield.value > 0 and not self.enemy.flag.condition_flag.buff_invincible_flag:
				self.enemy.condition.shield.value = 0
				self.champion.skill.para[2][0] = True
				print('触发破盾机制！')
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[1] * self.champion.attack_attribute.AD
			# 伤害计算
			self.Spell_attack_damage_calculation()
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
				# 眩晕效果处理
				if self.champion.skill.para[2][0]:
					dizz_time = self.champion.skill.para[2][2] / self.enemy.champion.defensive_attribute.tenacity
					self.champion.skill.para[2][0] = False
				else:
					dizz_time = self.champion.skill.para[2][1] / self.enemy.champion.defensive_attribute.tenacity
				if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
					dizz_time += self.flag.weapon_flag.jdzc[1]
					self.flag.weapon_flag.jdzc[2] = True
					self.flag.weapon_flag.jdzc[3] += 1
				self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 10阿木木
class Amumu(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 10
		self.champion.name = 'Amumu'
		self.champion.skill.name = '木乃伊之咒'
		self.champion.skill.describe = ['木乃伊之咒：阿木木迸发出怒火，对','周围的敌人造成100(+0.5*额外护甲)','魔法伤害，并使他们眩晕2.5s']
		self.champion.hp.max_value = 1050
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 125
		self.champion.attack_attribute.attack_speed = 0.57
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 50
		self.champion.defensive_attribute.spell_resistance = 15
		self.champion.relatedness.element[0] = '沙漠'
		self.champion.relatedness.profession[0] = '守护神'
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [100,2.5,0.5]
		self.champion.defensive_attribute.basic_armor = self.champion.defensive_attribute.armor
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			extra_armor = self.champion.defensive_attribute.armor - self.champion.defensive_attribute.basic_armor
			if extra_armor > 0:
				self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] + self.champion.skill.para[2] * extra_armor) * self.champion.attack_attribute.spell_power
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
				# 眩晕效果处理
				dizz_time = self.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
				if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
					dizz_time += self.flag.weapon_flag.jdzc[1]
					self.flag.weapon_flag.jdzc[2] = True
					self.flag.weapon_flag.jdzc[3] += 1
				self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
		if not self.flag.special_flag.dead_area[0]:
			# 周围伤害计算
			temp_enemy = self.enemy
			extra_armor = self.champion.defensive_attribute.armor - self.champion.defensive_attribute.basic_armor
			if extra_armor > 0:
				self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] + self.champion.skill.para[2] * extra_armor) * self.champion.attack_attribute.spell_power
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
				and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.special_flag.dead_area[0]):
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					else:
						self.Spell_attack_damage_calculation()
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
							# 眩晕效果处理
							dizz_time = self.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
							if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
								dizz_time += self.flag.weapon_flag.jdzc[1]
								self.flag.weapon_flag.jdzc[2] = True
							self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
			self.enemy = temp_enemy
			self.champion.skill.aoe[1] = False
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 11雷恩加尔
class Rengar(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 11
		self.champion.name = 'Rengar'
		self.champion.skill.name = '狩猎律动'
		self.champion.skill.describe = ['狩猎律动：雷恩加尔跃向护甲最低的','敌人对其进行背刺，使目标的护甲减','少10(最低减至0)并造成1.7*AD的物理','伤害+20*溢出削甲的真实伤害']
		self.champion.hp.max_value = 900
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 75
		self.champion.attack_attribute.attack_speed = 0.61
		self.champion.attack_attribute.AD = 50
		self.champion.defensive_attribute.armor = 34
		self.champion.defensive_attribute.spell_resistance = 24
		self.champion.relatedness.element[0] = '沙漠'
		self.champion.relatedness.profession[0] = '刺客'
		self.champion.attack_attribute.armor_penetration += 15
		self.champion.attack_attribute.spell_resistance_penetration += 15

		self.champion.skill.para = [10,1.7,20]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		am_min = self.enemy.champion.defensive_attribute.armor
		enemy_pos_number = 0
		for i in range(3):
			if (not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag) and (not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0]) \
			and not (self.game.LR[~self.position+2][i].flag.special_flag.dead_area[0] and not self.flag.special_flag.dead_area[0]) and self.game.LR[~self.position+2][i].champion.defensive_attribute.armor <= am_min:
				am_min = self.game.LR[~self.position+2][i].champion.defensive_attribute.armor
				enemy_pos_number = i
		self.enemy = self.game.LR[~self.position+2][enemy_pos_number]
		# 测试阿利斯塔吸引刺客效果
		for i in range(3):
			if self.game.LR[~self.position+2][i].champion.name == 'Alistar':
				Alistar = self.game.LR[~self.position+2][i]
				if not Alistar.flag.condition_flag.death_flag and not Alistar.flag.condition_flag.miss_flag[0] and Alistar.champion.skill.para[3]:
					self.enemy = Alistar
		# 死者领域内
		if self.flag.special_flag.dead_area[0]:
			self.enemy = self.flag.special_flag.dead_area[1]
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		# 处理伏击之爪
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[1] * self.champion.attack_attribute.AD
			# 削甲效果处理
			#	幻影之舞免疫削甲
			if self.enemy.flag.weapon_flag.hyzw[0]:
				self.enemy.flag.weapon_flag.hyzw[1] = True											# 显示触发幻影之舞
			elif self.enemy.flag.condition_flag.buff_invincible_flag:								# 无敌状态免疫削甲
				pass
			else:
				if self.enemy.champion.defensive_attribute.armor - self.champion.skill.para[0] < 0: # 削甲溢出
					overflow_damage = (self.champion.skill.para[0] - self.enemy.champion.defensive_attribute.armor) * self.champion.skill.para[2]
					self.champion.attack_attribute.spell_attack.real_damage = overflow_damage * self.champion.attack_attribute.spell_power
					self.enemy.champion.defensive_attribute.armor = 0
				else:
					self.enemy.champion.defensive_attribute.armor -= self.champion.skill.para[0]
			# 伤害计算
			self.Spell_attack_damage_calculation()
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 12维迦
class Veigar(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 12
		self.champion.name = 'Veigar'
		self.champion.skill.name = '能量爆裂'
		self.champion.skill.describe = ['能量爆裂：维迦用源力魔法引爆目标，','造成180~360点魔法伤害，伤害提升幅','度基于目标的已损失生命值']
		self.champion.hp.max_value = 840
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.60
		self.champion.attack_attribute.AD = 34
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '森林'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['超凡邪力',['超凡邪力：维迦使用能量爆裂击杀敌','人时可以获得30%法强增幅','层数：0'],False]

		self.champion.skill.para = [180,0.3,0]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] + self.champion.skill.para[0] * ((self.enemy.champion.hp.max_value - \
				self.enemy.champion.hp.value)/self.enemy.champion.hp.max_value)) * self.champion.attack_attribute.spell_power
			# 伤害计算
			self.Spell_attack_damage_calculation()
			if self.enemy.flag.condition_flag.death_flag:
				self.champion.attack_attribute.spell_power += self.champion.skill.para[1]
				self.champion.skill.para[2] += 1
				self.champion.skill.extra[2][0][2] = True
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy

		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 13韦鲁斯
class Varus(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 13
		self.champion.name = 'Varus'
		self.champion.skill.name = '枯萎箭袋'
		self.champion.skill.describe = ['枯萎箭袋：韦鲁斯的普攻会附加20点','魔法伤害，并且每第4次攻击造成基于','(目标最大生命值)12%的额外魔法伤害']
		self.champion.skill.active_skill = False
		self.champion.hp.max_value = 870
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 0
		self.champion.mp.max_value = 0
		self.champion.attack_attribute.attack_speed = 0.73
		self.champion.attack_attribute.AD = 26
		self.champion.defensive_attribute.armor = 30
		self.champion.defensive_attribute.spell_resistance = 23
		self.champion.relatedness.element[0] = '水晶'
		self.champion.relatedness.profession[0] = '游侠'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['复仇之欲',['复仇之欲：韦鲁斯击杀敌人时获得额','外20%攻速','层数：0'],False]

		self.champion.attack_attribute.attack_count = 0                      		# 攻击计数值
		self.champion.skill.para = [20,0.12,0.2,0]
	def Spell_attack(self):
		pass
	# 普攻前特殊效果
	def Special_normal_attack(self):
		self.champion.attack_attribute.normal_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
		# 计算额外魔法伤害
		self.champion.attack_attribute.attack_count += 1
		if self.champion.attack_attribute.attack_count == 4:
			self.flag.move_flag.show_cast_spell[0] = True
			self.champion.attack_attribute.normal_attack.spell_damage += self.champion.skill.para[1] * self.enemy.champion.hp.max_value * self.champion.attack_attribute.spell_power
			self.champion.attack_attribute.attack_count = 0
	# 技能被动效果(技能特殊效果处理)
	def Kill_deal(self):
		for _ in range(self.flag.special_flag.kill[4]):
			self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[2])
			self.champion.skill.para[3] += 1
			self.champion.skill.extra[2][0][2] = True
# 14塔里克
class Taric(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 14
		self.champion.name = 'Taric'
		self.champion.skill.name = '宇宙之辉'
		self.champion.skill.describe = ['宇宙之辉：塔里克呼唤宇宙之辉，在','2s的延迟后，宇宙光辉降临，令塔里','克及其周围的队友处于无敌状态，持','续3s']
		self.champion.hp.max_value = 1000
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 45
		self.champion.mp.max_value = 175
		self.champion.attack_attribute.attack_speed = 0.55
		self.champion.attack_attribute.AD = 38
		self.champion.defensive_attribute.armor = 48
		self.champion.defensive_attribute.basic_armor = self.champion.defensive_attribute.armor
		self.champion.defensive_attribute.spell_resistance = 27
		self.champion.relatedness.element[0] = '水晶'
		self.champion.relatedness.profession[0] = '守护神'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['正气凌人',['正气凌人：处于无敌状态时，攻速翻','倍并且普攻附带20(+0.2*额外护甲)点','魔法伤害'],False]

		self.champion.skill.para = [False,Time_count(),2,3,[20,0.2,False]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 呼唤宇宙之辉
		self.champion.skill.para[0] = True
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[2]
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if self.champion.skill.para[0]:
			end_flag = self.champion.skill.para[1].Duration(self.champion.skill.para[2])
			if end_flag:
				if not self.flag.special_flag.dead_area[0]:
					numTF = [True, self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
					num_pos = [self.pos_num, self.pos_num - 1, self.pos_num +1]
					# 加无敌时间
					for i in range(3):
						if numTF[i] and (not self.game.LR[self.position][num_pos[i]].flag.condition_flag.death_flag) \
						and (not self.game.LR[self.position][num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[self.position][num_pos[i]].flag.special_flag.dead_area[0]):
							self.condition.invincible.Add_invincible(self.game.LR[self.position][num_pos[i]],self.champion.skill.para[3])
				else:
					self.condition.invincible.Add_invincible(self,self.champion.skill.para[3])
				self.champion.skill.para[0] = False
		if self.flag.condition_flag.buff_invincible_flag and not self.champion.skill.para[4][2]:
			self.champion.attack_attribute.attack_speed *= 2
			self.champion.skill.para[4][2] = True
			self.champion.skill.extra[2][0][2] = True
		elif not self.flag.condition_flag.buff_invincible_flag and self.champion.skill.para[4][2]:
			self.champion.attack_attribute.attack_speed /= 2
			self.champion.skill.para[4][2] = False
			self.champion.skill.extra[2][0][2] = False
	# 普攻前特殊效果：正气凌人
	def Special_normal_attack(self):
		if self.champion.skill.para[4][2]:
			extra_armor = self.champion.defensive_attribute.armor - self.champion.defensive_attribute.basic_armor
			if extra_armor <= 0:
				extra_armor = 0
			self.champion.attack_attribute.normal_attack.spell_damage += ((self.champion.skill.para[4][0] + self.champion.skill.para[4][1] \
				* extra_armor) * self.champion.attack_attribute.spell_power)
# 15菲兹
class Fizz(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 15
		self.champion.name = 'Fizz'
		self.champion.skill.name = '淘气打击'
		self.champion.skill.describe = ['淘气打击：菲兹向攻速最高的敌人进','行突刺，造成(0.5*AD)物理伤害和110','点魔法伤害，并触发普攻攻击特效']
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 45
		self.champion.mp.max_value = 60
		self.champion.attack_attribute.attack_speed = 0.66
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 28
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '海洋' if version[0] == 1 else '银河机神'
		self.champion.relatedness.profession[0] = '刺客'
		self.champion.attack_attribute.armor_penetration += 15
		self.champion.attack_attribute.spell_resistance_penetration += 15
		if version[0] == 3:
			self.champion.skill.extra[0] = True
			self.champion.skill.extra[1] = 1
			self.extra_skill = [['古灵',['古灵：菲兹在生命值低于150时跳上长','矛，处于不可选取状态，持续1.5s']],['精怪',['精怪：菲兹跳下长矛，对目标及其周','围敌人造成120点魔法伤害']]]
			self.champion.skill.extra[2][0][0] = self.extra_skill[0][0]
			self.champion.skill.extra[2][0][1] = self.extra_skill[0][1]
			self.champion.skill.extra[2][0][2] = True
			self.champion.skill.aoe[0] = True

		self.champion.skill.para = [0.5,110,1.5,120,150]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		as_max = self.enemy.champion.attack_attribute.attack_speed
		enemy_pos_number = 0
		for i in range(3):
			if (not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag) and (not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0])\
			and not (self.game.LR[~self.position+2][i].flag.special_flag.dead_area[0] and not self.flag.special_flag.dead_area[0]) and self.game.LR[~self.position+2][i].champion.attack_attribute.attack_speed >= as_max:
				as_max = self.game.LR[~self.position+2][i].champion.attack_attribute.attack_speed
				enemy_pos_number = i
		self.enemy = self.game.LR[~self.position+2][enemy_pos_number]
		# 测试阿利斯塔吸引刺客效果
		for i in range(3):
			if self.game.LR[~self.position+2][i].champion.name == 'Alistar':
				Alistar = self.game.LR[~self.position+2][i]
				if not Alistar.flag.condition_flag.death_flag and not Alistar.flag.condition_flag.miss_flag[0] and Alistar.champion.skill.para[3]:
					self.enemy = Alistar
		# 死者领域内
		if self.flag.special_flag.dead_area[0]:
			self.enemy = self.flag.special_flag.dead_area[1]
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			self.enemy.flag.weapon_flag.yzfr[2] = False
		# 处理伏击之爪
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		# 波比屏障效果
		elif self.enemy.flag.special_flag.obstacle_flag[0]:
			self.enemy.flag.special_flag.obstacle_flag[1].Obstacle(self)
		else:
			self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[0] * self.champion.attack_attribute.AD
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
			self.champion.attack_attribute.spell_attack.real_damage = 0
			# 触发攻击特效1
			self.Spell_special_effect1()
			# 伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 触发爆破专家羁绊效果
			if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
				self.champion.relatedness.Blast(self)
			self.Spell_special_effect2()
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 古灵精怪
	def Odd(self,mode):
		# 古灵
		if mode == 0:
			self.champion.skill.extra[2][0][2] = False
			self.champion.skill.extra[2][0][0] = self.extra_skill[1][0]
			self.champion.skill.extra[2][0][1] = self.extra_skill[1][1]
			self.champion.hp.value = self.champion.skill.para[4]
			self.condition.miss.Add_miss(self, self.champion.skill.para[2])
			self.flag.special_flag.odd[1] = True
			self.flag.special_flag.odd[0] = True
		# 精怪
		else:
			self.champion.skill.extra[2][0][2] = True
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.attack_attribute.spell_power
				# 中心伤害计算
				self.Spell_attack_damage_calculation()
				self.enemy.flag.special_flag.effect['古灵精怪'][0] = True
				if self.flag.damage_calculation_flag.spell_attack:
					if self.flag.weapon_flag.ldhs[0]: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
					# 触发爆破专家羁绊效果
					if self.flag.rela_flag['爆破专家'][0]:
						self.champion.relatedness.Blast(self)
			# 周围伤害计算
			temp_enemy = self.enemy
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.attack_attribute.spell_power
			numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				if numTF[i] and (not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.death_flag) \
				and (not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.miss_flag[0]):
					self.enemy = self.game.LR[~self.position+2][num_pos[i]]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					else:
						self.Spell_attack_damage_calculation()
						self.enemy.flag.special_flag.effect['古灵精怪'][0] = True
						if self.flag.damage_calculation_flag.spell_attack:
							# 触发爆破专家羁绊效果
							if self.flag.rela_flag['爆破专家'][0]:
								self.champion.relatedness.Blast(self)
				self.enemy = temp_enemy
			self.champion.skill.aoe[1] = False
# 16魔腾
class Nocturne(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 16
		self.champion.name = 'Nocturne'
		self.champion.skill.name = '鬼影重重'
		self.champion.skill.describe = ['鬼影重重：魔腾减少敌人视野，全队','处于完全闪避状态(持续3s)，然后飞','向生命最低的敌人，造成110(+1.4*额','外AD)点物理伤害']
		self.champion.hp.max_value = 880
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 130
		self.champion.mp.max_value = 155
		self.champion.attack_attribute.attack_speed = 0.66
		self.champion.attack_attribute.AD = 46
		self.champion.attack_attribute.basic_AD = self.champion.attack_attribute.AD
		self.champion.defensive_attribute.armor = 28
		self.champion.defensive_attribute.spell_resistance = 28
		self.champion.relatedness.element[0] = '森林'
		self.champion.relatedness.profession[0] = '刺客'
		self.champion.attack_attribute.armor_penetration += 15
		self.champion.attack_attribute.spell_resistance_penetration += 15
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['黑暗庇护',['黑暗庇护：魔腾施放鬼影重重后会获','得一个魔法护盾，持续4s'],False]

		self.champion.skill.para = [[False,Time_count(),3],[110,1.4],4]

	# 使用技能（施法）
	def Spell_attack(self):
		if not self.champion.skill.para[0][0]:
			if not self.flag.special_flag.dead_area[0]:
				# 天黑
				#sky_color[0] = black
				# 友军处于完全闪避状态
				for i in range(3):
					if (not self.friend[i].flag.condition_flag.death_flag) and (not self.friend[i].flag.special_flag.dead_area[0]):
						self.friend[i].champion.defensive_attribute.dodge_mechanism.all_dodge[2] = True
			else:
				self.champion.defensive_attribute.dodge_mechanism.all_dodge[2] = True
			self.champion.skill.para[0][0] = True
		# 判断目标
		hp_min = self.enemy.champion.hp.value + self.enemy.condition.shield.value
		enemy_pos_number = 0
		for i in range(3):
			if (not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag) and (not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0])\
			and not (self.game.LR[~self.position+2][i].flag.special_flag.dead_area[0] and not self.flag.special_flag.dead_area[0]) \
			and (self.game.LR[~self.position+2][i].champion.hp.value + self.game.LR[~self.position+2][i].condition.shield.value) <= hp_min:
				hp_min = self.game.LR[~self.position+2][i].champion.hp.value + self.game.LR[~self.position+2][i].condition.shield.value
				enemy_pos_number = i
		self.enemy = self.game.LR[~self.position+2][enemy_pos_number]
		# 阿利斯塔吸引刺客效果
		for i in range(3):
			if self.game.LR[~self.position+2][i].champion.name == 'Alistar':
				Alistar = self.game.LR[~self.position+2][i]
				if not Alistar.flag.condition_flag.death_flag and not Alistar.flag.condition_flag.miss_flag[0] and Alistar.champion.skill.para[3]:
					self.enemy = Alistar
		# 死者领域内
		if self.flag.special_flag.dead_area[0]:
			self.enemy = self.flag.special_flag.dead_area[1]
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		# 处理伏击之爪
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			extra_AD = self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD
			self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[1][0] + self.champion.skill.para[1][1] * extra_AD
			# 伤害计算
			self.Spell_attack_damage_calculation()
			# 加魔法护盾
			self.condition.magic_shield.Add_magic_shield(self,self.champion.skill.para[2])
			self.champion.skill.extra[2][0][2] = True

		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 解除完全闪避状态
		if self.champion.skill.para[0][0]:
			end_flag = self.champion.skill.para[0][1].Duration(self.champion.skill.para[0][2])
			if end_flag:
				for i in range(3):
					self.friend[i].champion.defensive_attribute.dodge_mechanism.all_dodge[2] = False
				self.champion.skill.para[0][0] = False
				#sky_color[0] = white

	# 特殊死亡处理
	def Death_deal_other(self):
		# 当鬼影重重期间魔腾死亡，则立刻恢复闪避率
		if self.champion.skill.para[0][0]:
			for i in range(3):
				self.friend[i].champion.defensive_attribute.dodge_mechanism.all_dodge[2] = False
			self.champion.skill.para[0][0] = False
			#sky_color[0] = white
# 17雷克塞
class RekSai(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 5
		self.champion.name = 'RekSai'
		self.champion.skill.name = ['遁地','破土而出']
		self.champion.skill.describe = [['遁地：雷克塞潜入土地之中，治疗自','身25%已损失生命值且处于60%减伤及','不可阻挡状态但不能攻击，持续2s'],['破土而出：雷克塞钻出地面，对敌人','造成100(+0.9*AD)的魔法伤害和2s眩晕','效果']]
		self.champion.hp.max_value = 980
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 150
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 49
		self.champion.defensive_attribute.armor = 41
		self.champion.defensive_attribute.spell_resistance = 23
		self.champion.relatedness.element[0] = '钢铁'
		self.champion.relatedness.profession[0] = '掠食者'

		self.champion.skill.comb[0] = True
		self.champion.skill.para = [False,[0.25,2,Time_count(),0.6],[100,0.9,2],0]
	# 使用技能（施法）
	def Spell_attack(self):
		# 遁地
		if self.champion.skill.comb[1] == 0:
			#print('遁地')
			# 治疗自己
			value_treatment = int((self.champion.skill.para[1][0] * (self.champion.hp.max_value - self.champion.hp.value)) * self.champion.attack_attribute.spell_power)
			self.champion.hp.HP_restore(value_treatment,self.champion,self)
			if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
				self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
				self.flag.weapon_flag.crxl[3] = True
			# 进入减伤及不可阻挡状态但不能行动
			matigation_value = 1 - self.champion.skill.para[1][3]
			self.condition.matigation.Add_matigation(self,matigation_value,self.champion.skill.para[1][1])
			self.condition.unstoppable.Add_unstoppable(self,self.champion.skill.para[1][1])
			self.champion.skill.para[0] = True
			self.champion.skill.comb[1] = 1 # 下一次施法是“破土而出”
			self.flag.move_flag.show_cast_spell[0] = True
		# 破土而出
		else:
			#print('破土而出')
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[2][0] + self.champion.skill.para[2][1] * self.champion.attack_attribute.AD) * self.champion.attack_attribute.spell_power
				# 伤害计算
				self.Spell_attack_damage_calculation()
				if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
					# 眩晕效果处理
					dizz_time = self.champion.skill.para[2][2] / self.enemy.champion.defensive_attribute.tenacity
					if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
						dizz_time += self.flag.weapon_flag.jdzc[1]
						self.flag.weapon_flag.jdzc[2] = True
						self.flag.weapon_flag.jdzc[3] += 1
					self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
			self.champion.skill.comb[1] = 0 # 下一次施法是“遁地”
			# 行为标志处理
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.cast_spell = False
			self.Special_spell_attack()
			self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 判断雷克塞遁地结束
		if self.champion.skill.para[0]:
			self.move.current_move = 'stop'
			end_flag = self.champion.skill.para[1][2].Duration(self.champion.skill.para[1][1])
			if end_flag:
				self.champion.skill.comb[3] = True
				self.champion.skill.para[0] = False
# 18奥拉夫
class Olaf(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 18
		self.champion.name = 'Olaf'
		self.champion.skill.name = '诸神黄昏'
		self.champion.skill.describe = ['诸神黄昏：奥拉夫移除身上所有控制','效果，6s内处于不可阻挡状态，获得','60%攻速和生命偷取(生命值<30%时为','120%)，但护甲、魔抗减半']
		self.champion.hp.max_value = 910
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 180
		self.champion.attack_attribute.attack_speed = 0.65
		self.champion.attack_attribute.AD = 50
		self.champion.defensive_attribute.armor = 38
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '极地'
		self.champion.relatedness.profession[0] = '狂战士'
		self.flag.special_flag.force_spell = True # 可强制施法

		self.flag.attack_speed_add_flag = True
		self.champion.skill.para = [6,[0.6,[False,0.3,1.2],0,0],False,Time_count()]

	# 使用技能（施法）
	def Spell_attack(self):
		# 移除所有控制效果(眩晕、冰冻、缴械)
		self.condition.dizz.Clean(self.flag,self)
		self.condition.frozen.Clean(self.flag,self)
		self.condition.disarm.Clean(self.flag,self)
		# 获得不可阻挡状态
		self.condition.unstoppable.Add_unstoppable(self,self.champion.skill.para[0])
		if not self.champion.skill.para[2]:
			# 提升攻速及生命偷取、减少护甲与魔抗
			if self.champion.hp.value < self.champion.skill.para[1][1][1] * self.champion.hp.max_value:
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[1][1][2])
				self.champion.hemophagia += self.champion.skill.para[1][1][2]
				self.champion.skill.para[1][1][0] = True
			else:
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[1][0])
				self.champion.hemophagia += self.champion.skill.para[1][0]
			self.champion.skill.para[1][2] = 0.5 * self.champion.defensive_attribute.armor
			self.champion.defensive_attribute.armor *= 0.5
			self.champion.skill.para[1][3] = 0.5 * self.champion.defensive_attribute.spell_resistance
			self.champion.defensive_attribute.spell_resistance *= 0.5
			self.champion.skill.para[2] = True
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 恢复攻速、生命偷取、护甲、魔抗
		if self.champion.skill.para[2]:
			end_flag = self.champion.skill.para[3].Duration(self.champion.skill.para[0])
			if end_flag:
				if self.champion.skill.para[1][1][0]:
					self.champion.attack_attribute.attack_speed /= (1 + self.champion.skill.para[1][1][2])
					self.champion.hemophagia -= self.champion.skill.para[1][1][2]
					self.champion.skill.para[1][1][0] = False
				else:
					self.champion.attack_attribute.attack_speed /= (1 + self.champion.skill.para[1][0])
					self.champion.hemophagia -= self.champion.skill.para[1][0]
				self.champion.defensive_attribute.armor += self.champion.skill.para[1][2]
				self.champion.defensive_attribute.spell_resistance += self.champion.skill.para[1][3]
				self.champion.skill.para[2] = False
# 19贾克斯
class Jax(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 16
		self.champion.name = 'Jax'
		self.champion.skill.name = '反击风暴'
		self.champion.skill.describe = ['反击风暴：贾克斯在4s内闪避所有普','攻，结束时对周围敌人进行打击，造','成50(+20*反击风暴时间内闪避普攻次','数)魔法伤害及1.5s眩晕']
		self.champion.hp.max_value = 930
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.61
		self.champion.attack_attribute.AD = 46
		self.champion.defensive_attribute.armor = 36
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '光'
		self.champion.relatedness.profession[0] = '狂战士'
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [[False,4,Time_count()],[50,20],1.5]

	# 使用技能（施法）
	def Spell_attack(self):
		# 进入完全闪避
		self.champion.defensive_attribute.dodge_mechanism.all_dodge[0] = True
		self.champion.skill.para[0][0] = True
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if self.champion.skill.para[0][0]:
			end_flag = self.champion.skill.para[0][2].Duration(self.champion.skill.para[0][1])
			if end_flag:
				if not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[1][0] + self.champion.skill.para[1][1] \
							* self.champion.defensive_attribute.dodge_mechanism.all_dodge[1]) * self.champion.attack_attribute.spell_power
						# 中心伤害计算
						self.Spell_attack_damage_calculation()
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
							# 眩晕效果处理
							dizz_time = self.champion.skill.para[2] / self.enemy.champion.defensive_attribute.tenacity
							if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
								dizz_time += self.flag.weapon_flag.jdzc[1]
								self.flag.weapon_flag.jdzc[2] = True
								self.flag.weapon_flag.jdzc[3] += 1
							self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
							if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
								self.flag.weapon_flag.ldhs[1] = True
								self.flag.weapon_flag.ldhs[4] = self.enemy
					if not self.flag.special_flag.dead_area[0]:
						# 周围伤害计算
						temp_enemy = self.enemy
						temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
						temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
						self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[1][0] + self.champion.skill.para[1][1] \
							* self.champion.defensive_attribute.dodge_mechanism.all_dodge[1]) * self.champion.attack_attribute.spell_power
						for i in range(2):
							if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
							and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.special_flag.dead_area[0]):
								self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
								# 处理敌人魔法护盾效果
								if self.enemy.flag.condition_flag.buff_magic_shield_flag:
									self.enemy.condition.magic_shield.Clean(self.enemy.flag)
								else:
									self.Spell_attack_damage_calculation()
									if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
										# 眩晕效果处理
										dizz_time = self.champion.skill.para[2] / self.enemy.champion.defensive_attribute.tenacity
										if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
											dizz_time += self.flag.weapon_flag.jdzc[1]
											self.flag.weapon_flag.jdzc[2] = True
											self.flag.weapon_flag.jdzc[3] += 1
										self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
						self.enemy = temp_enemy
						self.champion.skill.aoe[1] = False	
				# 处理标志位
				self.champion.defensive_attribute.dodge_mechanism.all_dodge[0] = False
				self.champion.defensive_attribute.dodge_mechanism.all_dodge[1] = 0
				self.champion.skill.para[0][0] = False
# 20娜美
class Nami(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 20
		self.champion.name = 'Nami'
		self.champion.skill.name = '冲击之潮'
		self.champion.skill.describe = ['冲击之潮：娜美释放一股在友方、敌','方和自己之间交替流动的水潮，目标','为友方或自己时治疗130生命值，目标','为敌方时造成100(+0.3*魔抗)魔法伤害']
		self.champion.hp.max_value = 870
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.61
		self.champion.attack_attribute.AD = 39
		self.champion.defensive_attribute.armor = 35
		self.champion.defensive_attribute.spell_resistance = 26
		self.champion.relatedness.element[0] = '海洋'
		self.champion.relatedness.profession[0] = '秘术师'
		# 水潮的间隔时间为0.7s
		self.champion.skill.para = [130,[100,0.3],0.7]
	# 使用技能（施法）
	def Spell_attack(self):
		# 释放水潮
		tide.Nami = self
		tide.flag = True
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 21布兰德
class Brand(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 21
		self.champion.name = 'Brand'
		self.champion.skill.name = '烈焰风暴'
		self.champion.skill.describe = ['烈焰风暴：布兰德发射一团火球在敌','人之间来回弹跳(最多5次)，对命中','的敌人每次造成90点魔法伤害']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.61
		self.champion.attack_attribute.AD = 33
		self.champion.defensive_attribute.armor = 26
		self.champion.defensive_attribute.spell_resistance = 24
		self.champion.relatedness.element[0] = '地狱火'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['火焰烙印',['火焰烙印：布兰德每次施放烈焰风暴','时，被火球命中三次的敌人将眩晕3s','触发次数：0'],False]
		# 火球的间隔时间为0.7s
		self.champion.skill.para = [90,3,0.7,False,0]
	# 使用技能（施法）
	def Spell_attack(self):
		# 若在死者领域内施法
		if self.flag.special_flag.dead_area[0]:
			self.champion.skill.para[3] = True
		else:
			self.champion.skill.para[3] = False
		# 发射火球
		fireball.Brand = self
		fireball.flag = True
		fireball.enemy = self.enemy
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 22拉克丝
class Lux(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 22
		self.champion.name = 'Lux'
		self.champion.hp.max_value = 840
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 110
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 35
		self.champion.defensive_attribute.armor = 27
		self.champion.defensive_attribute.spell_resistance = 20
		if version[0] == 1:
			ele_dic = {1 : '光', 2 : '极地', 3 : '森林', 4 : '水晶', 5 : '海洋', 6: '钢铁', 7 : '地狱火', 8 : '影'}
			n = 8
			self.champion.relatedness.element[0] = ele_dic[randint(1,n)]
		elif version[0] == 2:
			ele_dic = {1 : '云霄', 2 : '极地', 3 : '雷霆', 4 : '海洋', 5: '钢铁', 6 : '影'}
			n = 6
			self.champion.relatedness.element[0] = ele_dic[randint(1,n)]
		else:
			self.champion.relatedness.element[0] = '光'
		self.champion.relatedness.profession[0] = '大元素使'
		self.champion.skill.name = '终极闪光'
		self.champion.skill.describe = ['终极闪光：拉克丝发射一束元素爆裂','波，对敌人造成230点魔法伤害，若技','能击杀敌人，则回复60点法力值']
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['曲光屏障',['曲光屏障：每过10s，拉克丝向最远方','的队友掷出魔杖，魔杖会给拉克丝和','经过的队友加上60点护盾，持续2s，','魔杖返回时会再次获得护盾'],False]
		self.champion.skill.para = [[230,60],[60,2,Time_count(),10]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
			# 伤害计算
			self.Spell_attack_damage_calculation()
			# 击杀回蓝
			if self.enemy.flag.condition_flag.death_flag and not self.flag.special_flag.chakra_flag:
				self.champion.mp.Calculation(self,self.champion.skill.para[0][1])
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 曲光屏障
	def Special_effect_deal(self):
		end_flag = self.champion.skill.para[1][2].Duration(self.champion.skill.para[1][3])
		if end_flag:
			# 掷出魔杖
			wand.Lux = self
			wand.flag = True
			wand.mode = self.pos_num
			self.champion.skill.extra[2][0][2] = True
# 23科加斯
class ChoGath(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 23
		self.champion.name = 'ChoGath'
		self.champion.skill.name = '野性尖叫'
		self.champion.skill.describe = ['野性尖叫：科加斯施放恐怖声波，使','周围敌人沉默3s并造成90点魔法伤','害']
		self.champion.hp.max_value = 1100
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.56
		self.champion.attack_attribute.AD = 42
		self.champion.defensive_attribute.armor = 38
		self.champion.defensive_attribute.spell_resistance = 30
		self.champion.relatedness.element[0] = '影' if version[0] == 1 else '海洋'
		self.champion.relatedness.profession[0] = '掠食者'
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['肉食者',['肉食者：科加斯在击杀敌人时会回复','自身150点生命值和40点法力值','触发次数：0'],False]

		self.champion.skill.para = [3,90,150,40,0]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 沉默
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.special_flag.chakra_flag:
				self.condition.silence.Add_silence(self.enemy,self.champion.skill.para[0])
		if not self.flag.special_flag.dead_area[0]:
			# 周围伤害计算
			temp_enemy = self.enemy
			temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
				and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.special_flag.dead_area[0]):
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
						self.Spell_attack_damage_calculation()
						# 沉默
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.special_flag.chakra_flag:
							self.condition.silence.Add_silence(self.enemy,self.champion.skill.para[0])
			self.enemy = temp_enemy
			self.champion.skill.aoe[1] = False
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 击杀被动效果
	def Kill_deal(self):
		# 回复生命值
		value_treatment = self.champion.skill.para[2] * self.flag.special_flag.kill[4] * self.champion.attack_attribute.spell_power
		self.champion.hp.HP_restore(value_treatment, self.champion, self)
		if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
			self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
			self.flag.weapon_flag.crxl[3] = True
		# 回复法力值
		if not self.flag.special_flag.chakra_flag:
			mp_restore_value = self.champion.skill.para[3] * self.flag.special_flag.kill[4]
			self.champion.mp.Calculation(self,mp_restore_value)
		self.champion.skill.para[4] += 1
		self.champion.skill.extra[2][0][2] = True
# 24德莱厄斯
class Darius(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 24
		self.champion.name = 'Darius'
		self.champion.skill.name = '大杀四方'
		self.champion.skill.describe = ['大杀四方：在0.8s延迟后，德莱厄斯','向敌人挥舞斧头，造成60点魔法伤害','和1.0*AD的物理伤害，每命中一个敌','人，可以回复自身16%已损失生命值']
		self.champion.hp.max_value = 900
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 90
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 44
		self.champion.defensive_attribute.armor = 39
		self.champion.defensive_attribute.spell_resistance = 23
		self.champion.relatedness.element[0] = '钢铁'
		self.champion.relatedness.profession[0] = '狂战士'
		self.champion.skill.aoe[0] = True
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),0.8],[60,1.0],[0,0.16]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始施法
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[0][0].value = 0
			self.champion.skill.continuous[1] = True
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[0][1]
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
			# 施法结束
			if end_flag:
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1][0] * self.champion.attack_attribute.spell_power
					self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[1][1] * self.champion.attack_attribute.AD
					# 中心伤害计算
					self.Spell_attack_damage_calculation()
					# 命中敌人计数
					if self.flag.damage_calculation_flag.spell_attack:
						self.champion.skill.para[2][0] += 1
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
				if not self.flag.special_flag.dead_area[0]:
					# 周围伤害计算
					temp_enemy = self.enemy
					temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
					temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
					for i in range(2):
						if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
						and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.special_flag.dead_area[0]):
							self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
							# 处理敌人魔法护盾效果
							if self.enemy.flag.condition_flag.buff_magic_shield_flag:
								self.enemy.condition.magic_shield.Clean(self.enemy.flag)
							else:
								self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1][0] * self.champion.attack_attribute.spell_power
								self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[1][1] * self.champion.attack_attribute.AD
								self.Spell_attack_damage_calculation()
								# 命中敌人计数
								if self.flag.damage_calculation_flag.spell_attack:
									self.champion.skill.para[2][0] += 1
					self.enemy = temp_enemy
					self.champion.skill.aoe[1] = False
				# 回复生命值
				value_treatment = int(((self.champion.skill.para[2][1] * (self.champion.hp.max_value - self.champion.hp.value)) * self.champion.skill.para[2][0])* self.champion.attack_attribute.spell_power)
				self.champion.hp.HP_restore(value_treatment,self.champion,self)
				# 计数清零
				self.champion.skill.para[2][0] = 0
				if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
					self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
					self.flag.weapon_flag.crxl[3] = True

				self.champion.skill.continuous[1] = False
				self.champion.skill.continuous[2] = True
				# 行为标志处理
				self.flag.move_flag.cast_spell = False
				self.move.current_move = 'normal_attack'
# 25卡尔萨斯
class Karthus(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 25
		self.champion.name = 'Karthus'
		self.champion.skill.name = '安魂曲'
		self.champion.skill.describe = ['安魂曲：卡尔萨斯吟唱3s后，对所有','敌人造成220点魔法伤害']
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 130
		self.champion.attack_attribute.attack_speed = 0.60
		self.champion.attack_attribute.AD = 32
		self.champion.defensive_attribute.armor = 27
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '影'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.aoe[0] = True
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),3],220]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始施法
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[0][0].value = 0
			self.champion.skill.continuous[1] = True
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[0][1]
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
			# 施法结束
			if end_flag:
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
					# 中心伤害计算
					self.Spell_attack_damage_calculation()
					self.enemy.flag.special_flag.effect['安魂曲'][0] = True
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
				if not self.flag.special_flag.dead_area[0]:
					# 周围伤害计算
					temp_enemy = self.enemy
					for i in range(3):
						if self.game.LR[~self.position+2][i] != temp_enemy and (not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag) \
						and (not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][i].flag.special_flag.dead_area[0]):
							self.enemy = self.game.LR[~self.position+2][i]
							# 处理敌人魔法护盾效果
							if self.enemy.flag.condition_flag.buff_magic_shield_flag:
								self.enemy.condition.magic_shield.Clean(self.enemy.flag)
							else:
								self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
								self.Spell_attack_damage_calculation()
								self.enemy.flag.special_flag.effect['安魂曲'][0] = True
					self.enemy = temp_enemy
					self.champion.skill.aoe[1] = False
				self.champion.skill.continuous[1] = False
				self.champion.skill.continuous[2] = True
				# 行为标志处理
				self.flag.move_flag.cast_spell = False
				self.move.current_move = 'normal_attack'
# 26锤石
class Thresh(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 26
		self.champion.name = 'Thresh'
		self.champion.skill.name = '魂引之灯'
		self.champion.skill.describe = ['魂引之灯：锤石将他的灯笼扔到生命','值最低的友军处，为该友军提供180点','护盾、为附近的友军提供130点护盾，','持续5s']
		self.champion.hp.max_value = 910
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 130
		self.champion.attack_attribute.attack_speed = 0.64
		self.champion.attack_attribute.AD = 38
		self.champion.defensive_attribute.armor = 40
		self.champion.defensive_attribute.spell_resistance = 30
		self.champion.relatedness.element[0] = '地狱火' if version[0] == 1 else '海洋'
		self.champion.relatedness.profession[0] = '秘术师'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['地狱诅咒',['地狱诅咒：锤石击杀敌人时获得50点','护甲、提升30%法强','层数：0'],False]

		self.champion.skill.para = [[180,130],5,50,0.3,0]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		if not self.flag.special_flag.dead_area[0]:
			hp_min = self.champion.hp.value + self.condition.shield.value
			friend_pos_number = 0
			for i in range(3):
				if (not self.friend[i].flag.condition_flag.death_flag) and (not self.friend[i].flag.condition_flag.miss_flag[0]) and (not self.friend[i].flag.special_flag.dead_area[0])\
				and (self.friend[i].champion.hp.value + self.friend[i].condition.shield.value) <= hp_min:
					hp_min = self.friend[i].champion.hp.value + self.friend[i].condition.shield.value
					friend_pos_number = i
			temp_friend_numTF = [friend_pos_number - 1 >= 0, True ,friend_pos_number + 1 <= 2]
			temp_friend_num_pos = [friend_pos_number - 1, friend_pos_number, friend_pos_number + 1]
			for j in range(3):
				if temp_friend_numTF[j] and (not self.friend[temp_friend_num_pos[j]].flag.condition_flag.death_flag) and (not self.friend[temp_friend_num_pos[j]].flag.condition_flag.miss_flag[0])\
				and (not self.friend[temp_friend_num_pos[j]].flag.special_flag.dead_area[0]):
					# 获得护盾
					if j==1:
						shield_add = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
						self.condition.shield.Add_shield(self.friend[temp_friend_num_pos[j]],shield_add,self.champion.skill.para[1])
						self.friend[temp_friend_num_pos[j]].flag.special_flag.effect['魂引之灯'][0] = True
					else:
						shield_add = self.champion.skill.para[0][1] * self.champion.attack_attribute.spell_power
						self.condition.shield.Add_shield(self.friend[temp_friend_num_pos[j]],shield_add,self.champion.skill.para[1])
					if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
						self.condition.fervor.Add_fervor(self.friend[temp_friend_num_pos[j]],self.flag.weapon_flag.crxl[2][2])
						self.flag.weapon_flag.crxl[3] = True
		else:
			# 获得护盾
			shield_add = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
			self.condition.shield.Add_shield(self,shield_add,self.champion.skill.para[1])
			self.flag.special_flag.effect['魂引之灯'][0] = True
			if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
				self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
				self.flag.weapon_flag.crxl[3] = True
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 击杀被动效果
	def Kill_deal(self):
		# 获得护甲
		self.champion.defensive_attribute.armor += self.champion.skill.para[2]
		# 提升法强
		self.champion.attack_attribute.spell_power += self.champion.skill.para[3]
		self.champion.skill.para[4] += 1
		self.champion.skill.extra[2][0][2] = True
		print('触发锤石被动：地狱诅咒')
# 27卡特琳娜
class Katarina(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 27
		self.champion.name = 'Katarina'
		self.champion.skill.name = '死亡莲华'
		self.champion.skill.describe = ['死亡莲华：卡特琳娜向生命最低的敌','人瞬移，化为剑刃飓风向周围投掷匕','首，每把造成25魔法伤害，总共在3s','内对每人造成250魔法伤害并令其重伤']
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 85
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 47
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '影'
		self.champion.relatedness.profession[0] = '刺客'
		self.champion.attack_attribute.armor_penetration += 15
		self.champion.attack_attribute.spell_resistance_penetration += 15
		self.champion.skill.aoe[0] = True
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),0.3,0,10],25,3,None]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始施法
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[0][0].value = 0
			self.champion.skill.para[0][2] = 0
			# 判断目标
			hp_min = self.enemy.champion.hp.value + self.enemy.condition.shield.value
			enemy_pos_number = 0
			for i in range(3):
				if (not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag) and (not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0])\
				and not (self.game.LR[~self.position+2][i].flag.special_flag.dead_area[0] and not self.flag.special_flag.dead_area[0]) \
				and (self.game.LR[~self.position+2][i].champion.hp.value + self.game.LR[~self.position+2][i].condition.shield.value) <= hp_min:
					enemy_pos_number = i
			self.enemy = self.game.LR[~self.position+2][enemy_pos_number]
			# 	阿利斯塔吸引刺客效果
			for i in range(3):
				if self.game.LR[~self.position+2][i].champion.name == 'Alistar':
					Alistar = self.game.LR[~self.position+2][i]
					if not Alistar.flag.condition_flag.death_flag and not Alistar.flag.condition_flag.miss_flag[0] and Alistar.champion.skill.para[3]:
						self.enemy = Alistar
			self.champion.skill.para[3] = self.enemy
			self.champion.skill.continuous[1] = True
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[0][1] * self.champion.skill.para[0][3]
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			#	目标死亡或无法选取则中断施法
			if self.champion.skill.para[3].flag.condition_flag.death_flag or self.champion.skill.para[3].flag.condition_flag.miss_flag[0]:
				self.champion.skill.para[0][0].value = 0
				self.champion.skill.continuous[3] = True
				print('%s持续施法期间目标%s死亡或不可选取，中断施法' %(self.champion.name,self.champion.skill.para[3].champion.name))
			else:
				end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
				# 伤害DOT
				if end_flag:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
						# 中心伤害计算
						self.Spell_attack_damage_calculation()
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack and self.champion.skill.para[0][2] == 0: # 触发卢登回声效果
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						# 重伤效果
						if self.flag.damage_calculation_flag.spell_attack:
							self.condition.injury.Add_injury(self.enemy, self.champion.skill.para[2])
					if not self.flag.special_flag.dead_area[0]:
						# 周围伤害计算
						temp_enemy = self.enemy
						temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
						temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
						for i in range(2):
							if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
							and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.special_flag.dead_area[0]):
								self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
								# 处理敌人魔法护盾效果
								if self.enemy.flag.condition_flag.buff_magic_shield_flag:
									self.enemy.condition.magic_shield.Clean(self.enemy.flag)
								else:
									self.flag.damage_calculation_flag.spell_attack = False
									self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
									self.Spell_attack_damage_calculation()
									# 重伤效果
									if self.flag.damage_calculation_flag.spell_attack:
										self.condition.injury.Add_injury(self.enemy, self.champion.skill.para[2])
						self.enemy = temp_enemy
						self.champion.skill.aoe[1] = False
					self.champion.skill.para[0][2] += 1
		if self.champion.skill.para[0][2] >= self.champion.skill.para[0][3] or self.champion.skill.continuous[3]:
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = False
			self.champion.skill.continuous[2] = True
			# 行为标志处理
			self.flag.move_flag.cast_spell = False
			self.move.current_move = 'normal_attack'
# 28莫德凯撒
class Mordekaiser(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 28
		self.champion.name = 'Mordekaiser'
		self.champion.skill.name = '轮回绝境'
		self.champion.skill.describe = ['轮回绝境：莫德凯撒将敌人放逐至死','者领域，造成100魔法伤害，7s内抽取','其部分属性并进行单挑，此期间敌人','死亡，莫德凯撒将永久获得偷取属性']
		self.champion.hp.max_value = 1000
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 105
		self.champion.mp.max_value = 145
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 44
		self.champion.defensive_attribute.armor = 44
		self.champion.defensive_attribute.spell_resistance = 24
		self.champion.relatedness.element[0] = '地狱火'
		self.champion.relatedness.profession[0] = '守护神'

		# 偷取属性：15%攻速、20%AD、20%护甲、20%魔抗、15%法强、10%暴击率、5%闪避率(其中攻速是乘法运算，所以其实不是偷取，只是此长彼消)
		self.champion.skill.para = [[Time_count(),7,False],[0.15,[0.2,0],[0.2,0],[0.2,0],[0.15,0],0.1,0.05],100]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标：
		#	首先判断友方是否有英雄遭受两个及以上敌人的攻击，并记录敌人的威胁系数(AD×攻速+额外威胁分)
		t1 = [[0,[None,0],[None,0],[None,0]] for _ in range(3)]
		for i in range(3):
			if self.friend[i] == self:
				continue
			for j in range(3):
				if self.game.LR[~self.position+2][j].enemy == self.friend[i] and self.game.LR[~self.position+2][j].champion.name != 'SolarDisk':
					t1[i][0] += 1
					t1[i][j+1][0] = self.game.LR[~self.position+2][j]
					t1[i][j+1][1] = t1[i][j+1][0].champion.attack_attribute.AD * t1[i][j+1][0].champion.attack_attribute.attack_speed + threat[t1[i][j+1][0].champion.name]
		enemy_temp = self.enemy
		self.enemy = None
		for i in range(3):
			# 先判断多打一的情况，选择其中威胁系数高的敌人作为目标
			if t1[i][0] > 1:
				threat_value_max = 0
				for j in range(3):
					if t1[i][j+1][0] != None and not t1[i][j+1][0].flag.condition_flag.death_flag and not t1[i][j+1][0].flag.condition_flag.miss_flag[0]:
						if t1[i][j+1][1] > threat_value_max:
							self.enemy = t1[i][j+1][0]
							threat_value_max = t1[i][j+1][1]
		# 否则则选择原来的攻击目标为目标
		if self.enemy == None:
			self.enemy = enemy_temp
		# 造成魔法伤害
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		# 处理伏击之爪
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[2] * self.champion.attack_attribute.spell_power
			# 伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 进入死者领域
			self.champion.skill.para[0][2] = True
			self.flag.special_flag.bless_land[0] = False
			self.enemy.flag.special_flag.bless_land[0] = False
			self.flag.special_flag.dead_area = [True,self.enemy]
			self.enemy.flag.special_flag.dead_area = [True,self]
			self.enemy.enemy = self
			# 偷取部分参数：
			#	攻速
			self.enemy.champion.attack_attribute.attack_speed *= (1 - self.champion.skill.para[1][0])
			self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[1][0])
			#	AD
			self.champion.skill.para[1][1][1] = self.champion.skill.para[1][1][0] * self.enemy.champion.attack_attribute.AD
			self.enemy.champion.attack_attribute.AD -= self.champion.skill.para[1][1][1]
			self.champion.attack_attribute.AD += self.champion.skill.para[1][1][1]
			#	护甲
			self.champion.skill.para[1][2][1] = self.champion.skill.para[1][2][0] * self.enemy.champion.defensive_attribute.armor
			self.enemy.champion.defensive_attribute.armor -= self.champion.skill.para[1][2][1]
			self.champion.defensive_attribute.armor += self.champion.skill.para[1][2][1]
			#	魔抗
			self.champion.skill.para[1][3][1] = self.champion.skill.para[1][3][0] * self.enemy.champion.defensive_attribute.spell_resistance
			self.enemy.champion.defensive_attribute.spell_resistance -= self.champion.skill.para[1][3][1]
			self.champion.defensive_attribute.spell_resistance += self.champion.skill.para[1][3][1]
			#	法强
			if self.enemy.champion.attack_attribute.spell_power - 1 >= self.champion.skill.para[1][4][0]:
				self.champion.skill.para[1][4][1] = self.champion.skill.para[1][4][0]
			else:
				self.champion.skill.para[1][4][1] = self.enemy.champion.attack_attribute.spell_power - 1
			self.enemy.champion.attack_attribute.spell_power -= self.champion.skill.para[1][4][1]
			self.champion.attack_attribute.spell_power += self.champion.skill.para[1][4][1]
			#	暴击率
			self.enemy.champion.attack_attribute.crit_mechanism.crit -= self.champion.skill.para[1][5]
			self.champion.attack_attribute.crit_mechanism.crit += self.champion.skill.para[1][5]
			#	闪避率
			self.enemy.champion.defensive_attribute.dodge_mechanism.dodge -= self.champion.skill.para[1][6]
			self.champion.defensive_attribute.dodge_mechanism.dodge += self.champion.skill.para[1][6]

		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 返还属性
	def Restitution(self):
		#	攻速
		self.enemy.champion.attack_attribute.attack_speed /= (1 - self.champion.skill.para[1][0])
		self.champion.attack_attribute.attack_speed /= (1 + self.champion.skill.para[1][0])
		#	AD
		self.enemy.champion.attack_attribute.AD += self.champion.skill.para[1][1][1]
		self.champion.attack_attribute.AD -= self.champion.skill.para[1][1][1]
		self.champion.skill.para[1][1][1] = 0
		#	护甲
		self.enemy.champion.defensive_attribute.armor += self.champion.skill.para[1][2][1]
		self.champion.defensive_attribute.armor -= self.champion.skill.para[1][2][1]
		self.champion.skill.para[1][2][1] = 0
		#	魔抗
		self.enemy.champion.defensive_attribute.spell_resistance += self.champion.skill.para[1][3][1]
		self.champion.defensive_attribute.spell_resistance -= self.champion.skill.para[1][3][1]
		self.champion.skill.para[1][3][1] = 0
		#	法强
		self.enemy.champion.attack_attribute.spell_power += self.champion.skill.para[1][4][1]
		self.champion.attack_attribute.spell_power -= self.champion.skill.para[1][4][1]
		self.champion.skill.para[1][4][1] = 0
		#	暴击率
		self.enemy.champion.attack_attribute.crit_mechanism.crit += self.champion.skill.para[1][5]
		self.champion.attack_attribute.crit_mechanism.crit -= self.champion.skill.para[1][5]
		#	闪避率
		self.enemy.champion.defensive_attribute.dodge_mechanism.dodge += self.champion.skill.para[1][6]
		self.champion.defensive_attribute.dodge_mechanism.dodge -= self.champion.skill.para[1][6]
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 判断是否结束
		if self.champion.skill.para[0][2]:
			end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
			if end_flag and not self.flag.special_flag.dead_area[1].flag.condition_flag.death_flag:
				# 返还属性
				self.Restitution()
				# 退出死者领域
				self.champion.skill.para[0][2] = False
				self.flag.special_flag.dead_area[0] = False
				self.flag.special_flag.dead_area[1].flag.special_flag.dead_area[0] = False
			elif self.flag.special_flag.dead_area[1].flag.condition_flag.death_flag:
				self.champion.skill.para[0][0].value = 0
				# 退出死者领域
				self.champion.skill.para[0][2] = False
				self.flag.special_flag.dead_area[0] = False
	# 特殊死亡处理
	def Death_deal_other(self):
		if self.flag.special_flag.dead_area[1] != None:
			if not self.flag.special_flag.dead_area[1].flag.condition_flag.death_flag and self.flag.special_flag.dead_area[1].flag.special_flag.dead_area[0]:
				# 当莫德凯撒在技能期间死亡，则返还目标属性并令目标退出死者领域
				print('莫德凯撒死亡特殊处理，%s退出死者领域' % self.flag.special_flag.dead_area[1].champion.name)
				#	返还属性
				self.Restitution()
				#	目标退出死者领域
				self.flag.special_flag.dead_area[1].flag.special_flag.dead_area[0] = False
# 29千珏
class Kindred(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 29
		self.champion.name = 'Kindred'
		self.champion.skill.name = '乱箭之舞'
		self.champion.skill.describe = ['乱箭之舞：千珏朝周围敌人发射最多','3支箭支，每支造成50(+1.0*额外AD)','物理伤害与50魔法伤害，并触发普攻','攻击特效']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 90
		self.champion.attack_attribute.attack_speed = 0.73
		self.champion.attack_attribute.AD = 48
		self.champion.defensive_attribute.armor = 30
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '黯焰'
		self.champion.relatedness.profession[0] = '游侠'
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 2
		self.champion.skill.extra[2][0] = ['千珏之印',['千珏之印：在开局时，千珏会随机标','记一个敌人，若千珏成功击杀该目标，','则提升20AD、25%攻速、30%法强','未触发'],False]
		self.champion.skill.extra[2][1] = ['羊灵生息',['羊灵生息：友方英雄生命低于10%时触','发，所有生灵进入赐福之土，生命值','最低降至10%，持续4s，结束时赐福之','土内的友军恢复120点生命值'],False]

		self.champion.skill.para = [[50,1.0],50,False,False,120,[Time_count(),4],[20,0.25,0.3,False]]
		self.champion.attack_attribute.basic_AD = self.champion.attack_attribute.AD
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[0][0] + self.champion.skill.para[0][1] * (self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD)
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_special_effect1()
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			self.Spell_special_effect2()
		if not self.flag.special_flag.dead_area[0]:
			# 周围伤害计算
			temp_enemy = self.enemy
			self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[0][0] + self.champion.skill.para[0][1] * (self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD)
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
			temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
				and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]) and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.special_flag.dead_area[0]):
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					else:
						self.Spell_special_effect1()
						self.Spell_attack_damage_calculation()
						self.Spell_special_effect2()
			self.enemy = temp_enemy
			self.champion.skill.aoe[1] = False
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 触发羊灵生息
	def Ylsx(self):
		self.champion.skill.para[2] = True
		self.champion.skill.para[3] = True
		if not self.flag.special_flag.dead_area[0]:
			for i in range(2):
				for j in range(3):
					if (not self.game.LR[i][j].flag.condition_flag.death_flag) and (not self.game.LR[i][j].flag.condition_flag.miss_flag[0])\
					and (not self.game.LR[i][j].flag.special_flag.dead_area[0]):
						self.game.LR[i][j].flag.special_flag.bless_land[0] = True
		else:
			f_or_e = [self.position,~self.position+2]
			for i in range(2):
				for j in range(3):
					if (not self.game.LR[f_or_e[i]][j].flag.condition_flag.death_flag) and (not self.game.LR[f_or_e[i]][j].flag.condition_flag.miss_flag[0])\
					and (not self.game.LR[f_or_e[i]][j].flag.special_flag.dead_area[0]):
						self.game.LR[f_or_e[i]][j].flag.special_flag.bless_land[0] = True
		self.champion.skill.extra[2][1][2] = True
	# 羊灵生息计时
	def Special_effect_deal(self):
		if self.champion.skill.para[2]:
			end_flag = self.champion.skill.para[5][0].Duration(self.champion.skill.para[5][1])
			if end_flag:
				# 友方回复生命值
				for i in range(3):
					if self.friend[i].flag.special_flag.bless_land[0] and not self.friend[i].flag.condition_flag.miss_flag[0]:
						self.friend[i].champion.hp.HP_restore(self.champion.skill.para[4],self.champion,self.friend[i])
						if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
							self.condition.fervor.Add_fervor(self.friend[i],self.flag.weapon_flag.crxl[2][2])
							self.flag.weapon_flag.crxl[3] = True
						self.friend[i].flag.special_flag.effect['羊灵生息'][0] = True
				self.champion.skill.para[2] = False
				for i in range(2):
					for j in range(3):
						self.game.LR[i][j].flag.special_flag.bless_land[0] = False
				self.champion.skill.extra[2][1][2] = False
	# 击杀处理
	def Kill_deal(self):
		for i in range(3):
			if self.flag.special_flag.kill[i+1] != None:
				if self.flag.special_flag.kill[i+1].flag.special_flag.Kindred_sign:
					self.champion.attack_attribute.AD += self.champion.skill.para[6][0]
					self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[6][1])
					self.champion.attack_attribute.spell_power += self.champion.skill.para[6][2]
					self.champion.skill.para[6][3] = True
					self.champion.skill.extra[2][0][2] = True
	# 特殊死亡处理：bug补丁
	def Death_deal_other(self):
		for i in range(2):
			for j in range(3):
				if self.game.LR[i][j].flag.special_flag.bless_land[0]:
					self.game.LR[i][j].flag.special_flag.bless_land[0] = False
# 30阿兹尔
class Azir(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 30
		self.champion.name = 'Azir'
		self.champion.skill.name = '沙兵现身'
		self.champion.skill.describe = ['沙兵现身：召唤黄沙士兵(上限3个，','持续10s)与阿兹尔同步攻击，每次造','成30点魔法伤害(属于技能伤害)']
		self.champion.hp.max_value = 870
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 50
		self.champion.attack_attribute.attack_speed = 0.7
		self.champion.attack_attribute.AD = 37
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '沙漠'
		self.champion.relatedness.profession[0] = '恕瑞玛之皇'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 2
		self.champion.skill.extra[2][0] = ['狂沙猛攻',['狂沙猛攻：同时存在三个沙兵时，阿','兹尔获得40%的攻速加成'],False]
		self.champion.skill.extra[2][1] = ['恕瑞玛的传承',['恕瑞玛的传承：阿兹尔将死亡的友军','献祭，延迟2s后召唤太阳圆盘，只能','召唤一次'],False]

		self.champion.skill.para = [30,10,0.4,False]
	
	# 使用技能（施法）
	def Spell_attack(self):
		# 召唤沙兵
		# 	在死者领域内施法
		if self.flag.special_flag.dead_area[0]:
			if not sand[self.pos_num].flag:
				sand[self.pos_num].flag = True
				sand[self.pos_num].position = self.position
				sand[self.pos_num].Azir = self
			else:
				sand[self.pos_num].time_count.value = 0
		#	在死者领域外施法
		else:
			pos_num = self.enemy.pos_num
			for i in range(3):
				if not sand[pos_num].flag:
					sand[pos_num].flag = True
					sand[pos_num].position = self.position
					sand[pos_num].Azir = self
					break
				else:
					pos_num += 1
					if pos_num == 3:
						pos_num = 0
					if self.game.LR[~self.position+2][pos_num].flag.special_flag.dead_area[0]:
						pos_num += 1
						if pos_num == 3:
							pos_num = 0
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 计算沙兵的持续时间&减伤状态判断
		for i in range(3):
			if sand[i].flag:
				end_flag = sand[i].time_count.Duration(self.champion.skill.para[1])
				if end_flag:
					sand[i].flag = False
			if self.game.LR[self.position][i].champion.relatedness.element[0] == '沙漠' and not self.game.LR[self.position][i].flag.condition_flag.death_flag and self.friend[i] != self:
				# 减伤效果
				matigation_value = 0.5
				self.condition.matigation.Add_matigation(self,matigation_value,0.5)
		# 狂沙猛攻判断
		if sand[0].flag and sand[1].flag and sand[2].flag:
			if not self.champion.skill.para[3]:
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[2])
				self.champion.skill.para[3] = True
				self.champion.skill.extra[2][0][2] = True
		else:
			if self.champion.skill.para[3]:
				self.champion.attack_attribute.attack_speed /= (1 + self.champion.skill.para[2])
				self.champion.skill.para[3] = False
				self.champion.skill.extra[2][0][2] = False
	# 特殊死亡处理
	def Death_deal_other(self):
		# 阿兹尔死亡时沙兵消失
		for i in range(3):
			sand[i].flag = False
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		# 处理沙兵攻击
		for i in range(3):
			if sand[i].flag:
				sand[i].Attack()
# 太阳圆盘
class SolarDisk(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 302
		self.champion.name = 'SolarDisk'
		self.champion.skill.name = '恕瑞玛的传承'
		self.champion.skill.describe = ['恕瑞玛的传承：太阳圆盘每次攻击后','增加5点AD']
		self.champion.hp.max_value = 700
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.skill.active_skill = False
		self.champion.mp.value = 0
		self.champion.mp.max_value = 0
		self.champion.attack_attribute.attack_speed = 0.66
		self.champion.attack_attribute.AD = 40
		self.champion.attack_attribute.crit_mechanism.crit = 0
		self.champion.attack_attribute.crit_mechanism.crit_multiple = 0
		self.champion.defensive_attribute.armor = 40
		self.champion.defensive_attribute.spell_resistance = 30
		self.champion.defensive_attribute.dodge_mechanism.dodge = 0
		self.champion.relatedness.element[0] = '沙漠'
		self.champion.relatedness.profession[0] = '太阳圆盘'

		self.champion.skill.para = [Time_count(),1,50,5]
	# 使用技能（施法）
	def Spell_attack(self):
		pass
	# 技能被动效果(技能特殊效果处理)
	def Special_effect_deal(self):
		self.flag.condition_flag.buff_unstoppable_flag = True
		end_flag = self.champion.skill.para[0].Duration(self.champion.skill.para[1])
		if end_flag:
			self.champion.hp.value -= self.champion.skill.para[2]
			if self.champion.hp.value <= 0:
				self.champion.hp.value = 0
				self.flag.condition_flag.death_flag = True
	# 特殊死亡处理
	def Death_deal_other(self):
		for i in range(3):
			if self.friend[i].champion.name == 'Azir':
				self.friend[i].champion.skill.extra[2][1][2] = False
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		# 太阳圆盘普攻叠AD
		self.champion.attack_attribute.AD += self.champion.skill.para[3]
SolarDisk = SolarDisk()

# S2
# 01-22拉克丝
# 02-2沃里克
# 03-23科加斯
# 04-26锤石
# 05-31奥莉安娜
class Orianna(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 31
		self.champion.name = 'Orianna'
		self.champion.skill.name = '指令_防卫'
		self.champion.skill.describe = ['指令_防卫：魔偶为附属的友军提供','200点护盾，持续4s；','被动：为附属的友军提供30点护甲、','30点魔抗']
		self.champion.hp.max_value = 840
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 10
		self.champion.mp.max_value = 80
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 30
		self.champion.defensive_attribute.armor = 28
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '影'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['指令_移动',['指令_移动：魔偶周期性移动，对途径','敌人造成10点魔法伤害；魔偶的位置','决定了奥莉安娜的指令(队友：防卫、','两端敌人：杂音、中心敌人：冲击波)'],False]

		self.champion.skill.para = [10,[200,4,30,30],[80],[[100,3],[80,1.5]]]
	# AOE伤害计算
	def AOE_damage(self,mode):
		temp_enemy = self.enemy
		self.enemy = self.game.LR[golem.position][golem.pos_num]
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			if mode == 1:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[2][0] * self.champion.attack_attribute.spell_power
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][0][0] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			if mode == 2:
				if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
					# 眩晕效果处理
					dizz_time = self.champion.skill.para[3][0][1] / self.enemy.champion.defensive_attribute.tenacity
					if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
						dizz_time += self.flag.weapon_flag.jdzc[1]
						self.flag.weapon_flag.jdzc[2] = True
						self.flag.weapon_flag.jdzc[3] += 1
					self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
		# 周围伤害计算
		temp_enemy2 = self.enemy
		if mode == 1:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[2][0] * self.champion.attack_attribute.spell_power
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][1][0] * self.champion.attack_attribute.spell_power
		temp_enemy_numTF = [temp_enemy2.pos_num - 1 >= 0, temp_enemy2.pos_num + 1 <= 2]
		temp_enemy_num_pos = [temp_enemy2.pos_num - 1, temp_enemy2.pos_num + 1]
		for i in range(2):
			if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
			and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]):
				self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				else:
					self.Spell_attack_damage_calculation()
					if mode == 2:
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
							# 眩晕效果处理
							dizz_time = self.champion.skill.para[3][1][1] / self.enemy.champion.defensive_attribute.tenacity
							if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
								dizz_time += self.flag.weapon_flag.jdzc[1]
								self.flag.weapon_flag.jdzc[2] = True
								self.flag.weapon_flag.jdzc[3] += 1
							self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
		self.enemy = temp_enemy
		self.champion.skill.aoe[1] = False
	# 使用技能（施法）
	def Spell_attack(self):
		if self.champion.skill.name == '指令_防卫':
			# 获得护盾
			shield_add = self.champion.skill.para[1][0] * self.champion.attack_attribute.spell_power
			self.condition.shield.Add_shield(self.friend[golem.pos_num],shield_add,self.champion.skill.para[1][1])
			if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
				self.condition.fervor.Add_fervor(self.friend[golem.pos_num],self.flag.weapon_flag.crxl[2][2])
				self.flag.weapon_flag.crxl[3] = True
		elif self.champion.skill.name == '指令_杂音':
			self.AOE_damage(1)
		elif self.champion.skill.name =='指令_冲击波':
			self.AOE_damage(2)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if not self.flag.move_flag.show_cast_spell[0]:
			if golem.position == self.enemy.position:
				if golem.pos_num == 1:
					self.champion.skill.name = '指令_冲击波'
					self.champion.skill.describe = ['指令_冲击波：魔偶释放强力冲击波，','对目标造成100点魔法伤害并眩晕3s，','对周围敌人造成80点魔法伤害并眩晕','1.5s']
				else:
					self.champion.skill.name = '指令_杂音'
					self.champion.skill.describe = ['指令_杂音：魔偶释放一股电脉冲，对','周围敌人造成80点魔法伤害']
			else:
				self.champion.skill.name = '指令_防卫'
				self.champion.skill.describe = ['指令_防卫：魔偶为附属的友军提供','200点护盾，持续4s；','被动：为附属的友军提供30点护甲、','30点魔抗']
	# 特殊死亡处理
	def Death_deal_other(self):
		golem.flag = False
# 06-32弗拉基米尔
class Vladimir(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 32
		self.champion.name = 'Vladimir'
		self.champion.skill.name = '鲜血转换'
		self.champion.skill.describe = ['鲜血转换：弗拉基米尔吸取敌人的生','命，造成110魔法伤害，治疗自身实际','造成伤害值；猩红冲刺：每第三次施','法时，伤害提升65%']
		self.champion.hp.max_value = 880
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 130
		self.champion.attack_attribute.attack_speed = 0.59
		self.champion.attack_attribute.AD = 32
		self.champion.defensive_attribute.armor = 29
		self.champion.defensive_attribute.spell_resistance = 24
		self.champion.relatedness.element[0] = '海洋'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['血红之池',['血红之池：弗拉基米尔在濒死时化成','一滩血池(无法选取状态，持续2s)，','并且立即准备施放下一次技能'],True]

		self.champion.skill.para = [110,[0,False],0.65,2]
	# 使用技能（施法）
	def Spell_attack(self):
		# 猩红冲刺计数
		self.champion.skill.para[1][1] = False
		self.champion.skill.para[1][0] += 1
		if self.champion.skill.para[1][0] == 3:
			self.champion.skill.para[1][1] = True
			self.champion.skill.para[1][0] = 0
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			if self.champion.skill.para[1][1]:
				self.champion.attack_attribute.spell_attack.spell_damage *= (1 + self.champion.skill.para[2])
			# 伤害计算
			self.Spell_attack_damage_calculation()
			# 获得治疗
			value_treatment = self.champion.attack_attribute.spell_attack_damage.total_damage
			self.champion.hp.HP_restore(value_treatment,self.champion,self)
			if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
				self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
				self.flag.weapon_flag.crxl[3] = True
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 血红之池
	def Blood(self):
		self.champion.skill.extra[2][0][2] = False
		self.champion.hp.value = 10
		self.condition.miss.Add_miss(self, self.champion.skill.para[3])
		self.flag.special_flag.blood_pool[1] = True
		self.flag.special_flag.blood_pool[0] = True
		# 回复满法力值
		self.champion.mp.value = self.champion.mp.max_value
# 07-33瑟庄妮
class Sejuani(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 33
		self.champion.name = 'Sejuani'
		self.champion.skill.name = '极冰寒狱'
		self.champion.skill.describe = ['极冰寒狱：瑟庄妮投出极冰套索，对','目标造成80点魔法伤害和4s冰冻效果，','2s后在目标周围产生冰风暴，对周围','敌人造成50点魔法伤害和2s冰冻效果']
		self.champion.hp.max_value = 950
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 35
		self.champion.mp.max_value = 130
		self.champion.attack_attribute.attack_speed = 0.56
		self.champion.attack_attribute.AD = 38
		self.champion.defensive_attribute.armor = 40
		self.champion.defensive_attribute.spell_resistance = 28
		self.champion.relatedness.element[0] = '极地'
		self.champion.relatedness.profession[0] = '守护神'
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['冰霜护甲',['冰霜护甲：瑟庄妮在开局后的12s内获','得35点额外护甲、35点额外魔抗，该','效果会在瑟庄妮击杀敌人时刷新'],False]

		self.champion.skill.para = [[80,4],[False,Time_count(),2,None],[50,2],[True,Time_count(),12],[False,35,35]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
				# 冰冻效果处理
				frozen_time = self.champion.skill.para[0][1] / self.enemy.champion.defensive_attribute.tenacity
				if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
					frozen_time += self.flag.weapon_flag.jdzc[1]
					self.flag.weapon_flag.jdzc[2] = True
					self.flag.weapon_flag.jdzc[3] += 1
				self.enemy.condition.frozen.Add_frozen(self.enemy,frozen_time)
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
		# 冰风暴准备
		self.champion.skill.para[1][0] = True
		self.champion.skill.para[1][3] = self.enemy
		self.enemy.flag.special_flag.effect['冰风暴'][0] = True

		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'	
		
	def Special_effect_deal(self):
		if self.champion.skill.para[3][0]:
			end_flag = self.champion.skill.para[3][1].Duration(self.champion.skill.para[3][2])
			if end_flag:
				self.champion.defensive_attribute.armor -= self.champion.skill.para[4][1]
				if self.champion.defensive_attribute.armor < 0:
					self.champion.defensive_attribute.armor = 0
				self.champion.defensive_attribute.spell_resistance -= self.champion.skill.para[4][2]
				if self.champion.defensive_attribute.spell_resistance < 0:
					self.champion.defensive_attribute.spell_resistance = 0
				self.champion.skill.para[4][0] = False
				self.champion.skill.para[3][0] = False
				self.champion.skill.extra[2][0][2] = False
			else:
				if not self.champion.skill.para[4][0]:
					self.champion.defensive_attribute.armor += self.champion.skill.para[4][1]
					self.champion.defensive_attribute.spell_resistance += self.champion.skill.para[4][2]
					self.champion.skill.para[4][0] = True
					self.champion.skill.extra[2][0][2] = True
	# 技能特殊效果处理2：与死亡状态无关
	def Special_effect_deal2(self):
		if self.champion.skill.para[1][0]:
			end_flag = self.champion.skill.para[1][1].Duration(self.champion.skill.para[1][2])
			if end_flag:
				# 周围伤害计算
				temp_enemy = self.enemy
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[2][0] * self.champion.attack_attribute.spell_power
				temp_enemy_numTF = [self.champion.skill.para[1][3].pos_num - 1 >= 0, self.champion.skill.para[1][3].pos_num + 1 <= 2]
				temp_enemy_num_pos = [self.champion.skill.para[1][3].pos_num - 1, self.champion.skill.para[1][3].pos_num + 1]
				for i in range(2):
					if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
					and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]):
						self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						else:
							self.Spell_attack_damage_calculation()
							if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
								# 冰冻效果处理
								frozen_time = self.champion.skill.para[2][1] / self.enemy.champion.defensive_attribute.tenacity
								if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
									frozen_time += self.flag.weapon_flag.jdzc[1]
									self.flag.weapon_flag.jdzc[2] = True
								self.enemy.condition.frozen.Add_frozen(self.enemy,frozen_time)
				self.champion.skill.para[1][3].flag.special_flag.effect['冰风暴'][0] = False
				self.champion.skill.para[1][0] = False
				self.enemy = temp_enemy
				self.champion.skill.aoe[1] = False
	# 击杀处理
	def Kill_deal(self):
		if not self.champion.skill.para[3][0]:
			self.champion.skill.para[3][0] = True
		else:
			self.champion.skill.para[3][1].value = 0
# 08-34凯尔
class Kayle(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 34
		self.champion.name = 'Kayle'
		self.champion.skill.name = '圣裁之刻'
		self.champion.skill.describe = ['圣裁之刻：凯尔为生命值最低友军施','加持续3s的无敌状态且其周身会受到','净化剑刃的庇护，结束时对周围敌人','造成80(+0.4*额外魔抗)的魔法伤害']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 110
		self.champion.attack_attribute.attack_speed = 0.65
		self.champion.attack_attribute.AD = 20
		self.champion.defensive_attribute.armor = 26
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.defensive_attribute.basic_spell_resistance = self.champion.defensive_attribute.spell_resistance
		self.champion.relatedness.element[0] = '银月'
		self.champion.relatedness.profession[0] = '秘术师'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['星火符刃',['星火符刃：凯尔的普通攻击会附加15','(+0.1*AD)额外魔法伤害，经过21s后','变为真实伤害且增加15%攻速'],False]
		self.champion.skill.aoe[0] = True
		self.champion.skill.para = [[False,None,3],[80,0.4],[15,0.1],21,[False,0.15]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		hp_min = self.champion.hp.value + self.condition.shield.value
		friend_pos_number = 0
		for i in range(3):
			if not self.friend[i].flag.condition_flag.death_flag and not self.friend[i].flag.condition_flag.miss_flag[0] \
			and not self.friend[i].flag.condition_flag.suppress[0] and (self.friend[i].champion.hp.value + self.friend[i].condition.shield.value) <= hp_min:
				hp_min = self.friend[i].champion.hp.value + self.friend[i].condition.shield.value
				friend_pos_number = i
		target = self.friend[friend_pos_number]
		# 圣裁之刻
		self.champion.skill.para[0][0] = True
		self.champion.skill.para[0][1] = target
		self.condition.invincible.Add_invincible(target,self.champion.skill.para[0][2])
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal2(self):
		if self.champion.skill.para[0][0]:
			# 无敌状态结束
			if not self.champion.skill.para[0][1].flag.condition_flag.buff_invincible_flag:
				temp_enemy = self.enemy
				self.enemy = self.champion.skill.para[0][1].enemy
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					extra_spell_resistance = self.champion.defensive_attribute.spell_resistance - self.champion.defensive_attribute.basic_spell_resistance
					self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[1][0] + self.champion.skill.para[1][1] * extra_spell_resistance) * self.champion.attack_attribute.spell_power
					# 中心伤害计算
					self.Spell_attack_damage_calculation()
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
					self.enemy.flag.special_flag.effect['净化剑刃'][0] = True
				# 周围伤害计算
				temp_enemy2 = self.enemy
				extra_spell_resistance = self.champion.defensive_attribute.spell_resistance - self.champion.defensive_attribute.basic_spell_resistance
				self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[1][0] + self.champion.skill.para[1][1] * extra_spell_resistance) * self.champion.attack_attribute.spell_power
				temp_enemy_numTF = [temp_enemy2.pos_num - 1 >= 0, temp_enemy2.pos_num + 1 <= 2]
				temp_enemy_num_pos = [temp_enemy2.pos_num - 1, temp_enemy2.pos_num + 1]
				for i in range(2):
					if temp_enemy_numTF[i] and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag) \
					and (not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]):
						self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						else:
							self.Spell_attack_damage_calculation()
							self.enemy.flag.special_flag.effect['净化剑刃'][0] = True
				self.enemy = temp_enemy
				self.champion.skill.aoe[1] = False
				self.champion.skill.para[0][0] = False
	# 普攻前特殊效果：星火符刃
	def Special_normal_attack(self):
		if self.game.time >= self.champion.skill.para[3]:
			if not self.champion.skill.para[4][0]:
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[4][1])
				self.champion.skill.para[4][0] = True
			self.champion.skill.extra[2][0][2] = True
			self.champion.attack_attribute.normal_attack.real_damage +=  ((self.champion.skill.para[2][0] + self.champion.skill.para[2][1] * \
				self.champion.attack_attribute.AD) * self.champion.attack_attribute.spell_power)
		else:
			self.champion.attack_attribute.normal_attack.spell_damage +=  ((self.champion.skill.para[2][0] + self.champion.skill.para[2][1] * \
				self.champion.attack_attribute.AD) * self.champion.attack_attribute.spell_power)
# 09-35迦娜
class Janna(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 35
		self.champion.name = 'Janna'
		self.champion.skill.name = '复苏季风'
		self.champion.skill.describe = ['复苏季风：迦娜在她周围召唤一阵季','风，在3s内持续治疗友军，数额为友','军自身的最大生命值的18%，附近的敌','人会被击退并且被晕眩0.5s']
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.63
		self.champion.attack_attribute.AD = 36
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 28
		self.champion.relatedness.element[0] = '云霄'
		self.champion.relatedness.profession[0] = '秘术师'
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),0.3,0,10],0.18,0.5]

	# 使用技能（施法）
	def Spell_attack(self):
		numTF = [True, self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
		num_pos = [self.pos_num, self.pos_num - 1, self.pos_num +1]
		# 开始施法
		if not self.champion.skill.continuous[1]:
			self.champion.skill.continuous[1] = True
			# 眩晕效果
			for i in range(3):
				if numTF[i] and not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.miss_flag[0]\
				and not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.buff_invincible_flag and not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.buff_unstoppable_flag:
					# 处理敌人魔法护盾效果(不触发伏击之爪)
					if self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.buff_magic_shield_flag:
						self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.buff_magic_shield_flag = False
					else:
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
							# 眩晕效果处理
							dizz_time = self.champion.skill.para[2] / self.game.LR[~self.position+2][num_pos[i]].champion.defensive_attribute.tenacity
							if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
								dizz_time += self.flag.weapon_flag.jdzc[1]
								self.flag.weapon_flag.jdzc[2] = True
								self.flag.weapon_flag.jdzc[3] += 1
							self.game.LR[~self.position+2][num_pos[i]].condition.dizz.Add_dizz(self.game.LR[~self.position+2][num_pos[i]],dizz_time)
			self.flag.move_flag.show_cast_spell = [True,self.champion.skill.para[0][1]*self.champion.skill.para[0][3]]
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
			# 回血DOT
			if end_flag:
				for i in range(3):
					if numTF[i] and not self.game.LR[self.position][num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[self.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
						hp_restore_value = (self.game.LR[self.position][num_pos[i]].champion.hp.max_value * ((self.champion.skill.para[1]) / self.champion.skill.para[0][3])) * self.champion.attack_attribute.spell_power
						self.game.LR[self.position][num_pos[i]].champion.hp.HP_restore(hp_restore_value, self.champion, self.game.LR[self.position][num_pos[i]])
						if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
							self.condition.fervor.Add_fervor(self.game.LR[self.position][num_pos[i]],self.flag.weapon_flag.crxl[2][2])
							self.flag.weapon_flag.crxl[3] = True
				self.champion.skill.para[0][2] += 1
		if self.champion.skill.para[0][2] >= self.champion.skill.para[0][3]:
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = False
			self.champion.skill.continuous[2] = True
			# 行为标志处理
			self.flag.move_flag.cast_spell = False
			self.move.current_move = 'normal_attack'	
# 10-36克格莫
class KogMaw(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 36
		self.champion.name = 'KogMaw'
		self.champion.skill.name = '活体大炮'
		self.champion.skill.describe = ['活体大炮：克格莫向随机一个敌人发','射一枚活体炮弹，对其造成100~200点','魔法伤害，伤害提升幅度基于目标的','已损失生命值']
		self.champion.hp.max_value = 830
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 45
		self.champion.attack_attribute.attack_speed = 0.67
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '剧毒'
		self.champion.relatedness.profession[0] = '掠食者'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['来自艾卡西亚的惊喜',['来自艾卡西亚的惊喜：死亡后，克格','莫的身体会开启连锁反应跑向最近的','敌人，3s后爆炸，造成150点真实伤害，','同时对周围敌人造成75点真实伤害'],False]
		self.champion.skill.aoe[0] = True
		self.champion.skill.para = [100,[False,None],[Time_count(),0.5],[150,75],False,[Time_count(),3]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标：随机
		p = randint(0,2)
		self.champion.skill.para[1][1] = self.game.LR[~self.position+2][p]
		i = 3
		while i >= 0:
			if not self.game.LR[~self.position+2][p].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][p].flag.condition_flag.miss_flag[0]:
				self.champion.skill.para[1][1] = self.game.LR[~self.position+2][p]
				break
			else:
				p += 1
				if p == 3:
					p = 0
			i -= 1
		if i < 0:
			self.champion.skill.para[1][1] = self.enemy
		# 发射炮弹
		self.champion.skill.para[1][0] = True
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal2(self):
		# 活体大炮
		if self.champion.skill.para[1][0]:
			end_flag = self.champion.skill.para[2][0].Duration(self.champion.skill.para[2][1])
			if end_flag:
				# 炮弹落地
				temp_enemy = self.enemy
				self.enemy = self.champion.skill.para[1][1]
				# 	若目标死亡或不可选取
				if self.enemy.flag.condition_flag.death_flag or self.enemy.flag.condition_flag.miss_flag[0]:
					self.enemy.flag.special_flag.effect['活体大炮'][0] = True
				else:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] + self.champion.skill.para[0] * \
							((self.enemy.champion.hp.max_value - self.enemy.champion.hp.value)/self.enemy.champion.hp.max_value)) * \
							self.champion.attack_attribute.spell_power
						# 伤害计算
						self.Spell_attack_damage_calculation()
						# 剧毒羁绊效果
						if self.flag.damage_calculation_flag.spell_attack and self.flag.rela_flag['剧毒'][0] and not self.enemy.flag.condition_flag.buff_invincible_flag\
						 and self.enemy.champion.skill.active_skill and not self.enemy.flag.special_flag.chakra_flag:
							self.enemy.condition.poisoning.Add_poisoning(self.enemy,rela_dic['剧毒'][1][2],self.flag.rela_flag['剧毒'][1]-2)
							self.flag.rela_flag['剧毒'][2][0] = True
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						self.enemy.flag.special_flag.effect['活体大炮'][0] = True
						self.champion.skill.para[1][0] = False
					self.enemy = temp_enemy
		# 来自艾卡西亚的惊喜
		if self.champion.skill.para[4]:
			end_flag = self.champion.skill.para[5][0].Duration(self.champion.skill.para[5][1])
			if end_flag:
				# 判断目标
				p = self.pos_num
				i = 3
				while i >= 0:
					if not self.game.LR[~self.position+2][p].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][p].flag.condition_flag.miss_flag[0]:
						self.enemy = self.game.LR[~self.position+2][p]
						break
					else:
						p += 1
						if p == 3:
							p = 0
					i -= 1
				if i < 0:
					self.enemy = self.game.LR[~self.position][self.pos_num]
				# 爆炸
				# 	处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
				else:
					self.champion.attack_attribute.spell_attack.real_damage = self.champion.skill.para[3][0] * self.champion.attack_attribute.spell_power
					# 中心伤害计算
					self.Spell_attack_damage_calculation()
					# 剧毒羁绊效果
					if self.flag.damage_calculation_flag.spell_attack and self.flag.rela_flag['剧毒'][0] and not self.enemy.flag.condition_flag.buff_invincible_flag \
					and self.enemy.champion.skill.active_skill and not self.enemy.flag.special_flag.chakra_flag:
						self.enemy.condition.poisoning.Add_poisoning(self.enemy,rela_dic['剧毒'][1][2],self.flag.rela_flag['剧毒'][1]-2)
						self.flag.rela_flag['剧毒'][2][0] = True
					self.enemy.flag.special_flag.effect['来自艾卡西亚的惊喜'][0] = True
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
				# 周围伤害计算
				temp_enemy = self.enemy
				self.champion.attack_attribute.spell_attack.real_damage = self.champion.skill.para[3][1] * self.champion.attack_attribute.spell_power
				temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
				temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
				for i in range(2):
					if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
						self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						else:
							self.Spell_attack_damage_calculation()
							# 剧毒羁绊效果
							if self.flag.damage_calculation_flag.spell_attack and self.flag.rela_flag['剧毒'][0] and not self.enemy.flag.condition_flag.buff_invincible_flag \
							and self.enemy.champion.skill.active_skill and not self.enemy.flag.special_flag.chakra_flag:
								self.enemy.condition.poisoning.Add_poisoning(self.enemy,rela_dic['剧毒'][1][2],self.flag.rela_flag['剧毒'][1]-2)
								self.flag.rela_flag['剧毒'][2][0] = True
							self.enemy.flag.special_flag.effect['来自艾卡西亚的惊喜'][0] = True
				self.enemy = temp_enemy
				self.champion.skill.aoe[1] = False
				self.champion.skill.extra[2][0][2] = False
				self.champion.skill.para[4] = False
	# 特殊死亡处理
	def Death_deal_other(self):
		self.champion.skill.para[4] = True
		self.champion.skill.extra[2][0][2] = True
# 11-37卡西奥佩娅
class Cassiopeia(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 37
		self.champion.name = 'Cassiopeia'
		self.champion.skill.name = '石化凝视'
		self.champion.skill.describe = ['石化凝视：卡西奥佩娅对敌人进行死','亡凝视，对范围内敌人造成110魔法伤','害(对中毒敌人造成1.2倍伤害)并石化','(即眩晕)2s']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 150
		self.champion.attack_attribute.attack_speed = 0.61
		self.champion.attack_attribute.AD = 32
		self.champion.defensive_attribute.armor = 27
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '剧毒'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['双生毒牙',['双生毒牙：卡西奥佩娅对中毒的敌人','进行普攻时，附加15点魔法伤害，并','治疗自身3%最大生命值'],False]

		self.champion.skill.para = [110,1.2,2,15,0.03,False]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			if self.enemy.flag.condition_flag.debuff_poisoning_flag:
				self.champion.attack_attribute.spell_attack.spell_damage *= self.champion.skill.para[1]
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			# 剧毒羁绊效果
			if self.flag.damage_calculation_flag.spell_attack and self.flag.rela_flag['剧毒'][0] and not self.enemy.flag.condition_flag.buff_invincible_flag \
			and self.enemy.champion.skill.active_skill and not self.enemy.flag.special_flag.chakra_flag:
				self.enemy.condition.poisoning.Add_poisoning(self.enemy,rela_dic['剧毒'][1][2],self.flag.rela_flag['剧毒'][1]-2)
				self.flag.rela_flag['剧毒'][2][0] = True
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 石化(眩晕)
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.champion.skill.para[2] / self.enemy.champion.defensive_attribute.tenacity
				if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
					dizz_time += self.flag.weapon_flag.jdzc[1]
					self.flag.weapon_flag.jdzc[2] = True
					self.flag.weapon_flag.jdzc[3] += 1
				self.condition.dizz.Add_dizz(self.enemy,dizz_time)
		# 周围伤害计算
		temp_enemy = self.enemy
		temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
		temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
		for i in range(2):
			if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
			and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
				self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
					if self.enemy.flag.condition_flag.debuff_poisoning_flag:
						self.champion.attack_attribute.spell_attack.spell_damage *= self.champion.skill.para[1]
					self.Spell_attack_damage_calculation()
					# 剧毒羁绊效果
					if self.flag.damage_calculation_flag.spell_attack and self.flag.rela_flag['剧毒'][0] and not self.enemy.flag.condition_flag.buff_invincible_flag \
					and self.enemy.champion.skill.active_skill and not self.enemy.flag.special_flag.chakra_flag:
						self.enemy.condition.poisoning.Add_poisoning(self.enemy,rela_dic['剧毒'][1][2],self.flag.rela_flag['剧毒'][1]-2)
						self.flag.rela_flag['剧毒'][2][0] = True
					# 石化(眩晕)
					if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.champion.skill.para[2] / self.enemy.champion.defensive_attribute.tenacity
						if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
							dizz_time += self.flag.weapon_flag.jdzc[1]
							self.flag.weapon_flag.jdzc[2] = True
							self.flag.weapon_flag.jdzc[3] += 1
						self.condition.dizz.Add_dizz(self.enemy,dizz_time)
		self.enemy = temp_enemy
		self.champion.skill.aoe[1] = False
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 普攻前特殊效果
	def Special_normal_attack(self):
		self.champion.skill.para[5] = False
		if self.enemy.flag.condition_flag.debuff_poisoning_flag[0]:
			self.champion.skill.extra[2][0][2] = True
			self.champion.skill.para[5] = True
			# 附加额外魔法伤害
			self.champion.attack_attribute.normal_attack.spell_damage += (self.champion.skill.para[3] * self.champion.attack_attribute.spell_power)
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		if self.champion.skill.para[5]:
			# 治疗自身
			value_treatment = self.champion.skill.para[4] * self.champion.hp.max_value * self.champion.attack_attribute.spell_power
			self.champion.hp.HP_restore(value_treatment,self.champion,self)
			if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
				self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
				self.flag.weapon_flag.crxl[3] = True
# 12-38蒙多
class Mundo(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 38
		self.champion.name = 'Mundo'
		self.champion.skill.name = '肾上腺激素'
		self.champion.skill.describe = ['肾上腺激素：蒙多医生创造一团持续','6s的护体毒雾，每秒对附近的敌人造','成1.8%蒙多最大生命值的魔法伤害，','回复1.5倍造成伤害数值的生命值']
		self.champion.hp.max_value = 1100
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 165
		self.champion.attack_attribute.attack_speed = 0.55
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 33
		self.champion.defensive_attribute.spell_resistance = 30
		self.champion.relatedness.element[0] = '剧毒'
		self.champion.relatedness.profession[0] = '斗士'
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [False,[Time_count(),1],[0,6],0.018,1.5]

	# 使用技能（施法）
	def Spell_attack(self):
		# 进入毒雾状态
		if not self.champion.skill.para[0]:
			self.champion.skill.para[0] = True
			self.flag.special_flag.toxic_smog = True
		else:# 重置时间
			self.champion.skill.para[1][0].value = 0
			self.champion.skill.para[2][0] = 0
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if self.champion.skill.para[0]:
			end_flag = self.champion.skill.para[1][0].Duration(self.champion.skill.para[1][1])
			if end_flag:
				# 计算伤害和回复
				if not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.hp.max_value * self.champion.attack_attribute.spell_power
						# 中心伤害计算
						self.Spell_attack_damage_calculation()
						# 回复生命值
						value_treatment = self.champion.skill.para[4] * self.champion.attack_attribute.spell_attack_damage.total_damage
						self.champion.hp.HP_restore(value_treatment,self.champion,self)
						if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
							self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
							self.flag.weapon_flag.crxl[3] = True
						# 剧毒羁绊效果
						if self.flag.damage_calculation_flag.spell_attack and self.flag.rela_flag['剧毒'][0] and not self.enemy.flag.condition_flag.buff_invincible_flag \
						and self.enemy.champion.skill.active_skill and not self.enemy.flag.special_flag.chakra_flag:
							self.enemy.condition.poisoning.Add_poisoning(self.enemy,rela_dic['剧毒'][1][2],self.flag.rela_flag['剧毒'][1]-2)
							self.flag.rela_flag['剧毒'][2][0] = True
						# 仅第一段伤害触发卢登回声效果
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack and self.champion.skill.para[2][0] == 0: 
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
					# 周围伤害计算
					temp_enemy = self.enemy
					temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
					temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.hp.max_value * self.champion.attack_attribute.spell_power
					for i in range(2):
						if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
						and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
							self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
							# 处理敌人魔法护盾效果
							if self.enemy.flag.condition_flag.buff_magic_shield_flag:
								self.enemy.condition.magic_shield.Clean(self.enemy.flag)
							else:
								self.Spell_attack_damage_calculation()
								# 回复生命值
								value_treatment = self.champion.skill.para[4] * self.champion.attack_attribute.spell_attack_damage.total_damage
								self.champion.hp.HP_restore(value_treatment,self.champion,self)
								if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
									self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
									self.flag.weapon_flag.crxl[3] = True
								# 剧毒羁绊效果
								if self.flag.damage_calculation_flag.spell_attack and self.flag.rela_flag['剧毒'][0] and not self.enemy.flag.condition_flag.buff_invincible_flag \
								and self.enemy.champion.skill.active_skill and not self.enemy.flag.special_flag.chakra_flag:
									self.enemy.condition.poisoning.Add_poisoning(self.enemy,rela_dic['剧毒'][1][2],self.flag.rela_flag['剧毒'][1]-2)
									self.flag.rela_flag['剧毒'][2][0] = True
					self.enemy = temp_enemy
					self.champion.skill.aoe[1] = False	
				# DOT计数
				self.champion.skill.para[2][0] += 1
				if self.champion.skill.para[2][0] == self.champion.skill.para[2][1]:
					self.champion.skill.para[2][0] = 0
					self.champion.skill.para[0] = False
					self.flag.special_flag.toxic_smog = False
# 13-39奥恩
class Ornn(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 39
		self.champion.name = 'Ornn'
		self.champion.skill.name = '雷霆吐息'
		self.champion.skill.describe = ['雷霆吐息：奥恩向前吐息雷霆风暴，','0.9s内不可阻挡，打出3段(5%/5%/8%)','敌人最大生命值魔法伤害，第3段伤害','后令敌人处于感电状态(持续3.5s)']
		self.champion.hp.max_value = 960
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 90
		self.champion.attack_attribute.attack_speed = 0.58
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 39
		self.champion.defensive_attribute.spell_resistance = 27
		self.champion.relatedness.element[0] = '雷霆'
		self.champion.relatedness.profession[0] = '守护神'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['工匠大师',['工匠大师：奥恩会为队友升级武器(只','限于12种特定武器)'],False]
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),0.3],[0,3],0.9,[0.05,0.08],3.5,False,None]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始施法
		if not self.champion.skill.continuous[1]:
			self.champion.skill.continuous[1] = True
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[2]
			self.champion.skill.para[6] = self.enemy
			# 不可阻挡状态：所以不会被控制打断施法，但会被沉默打断施法
			self.condition.unstoppable.Add_unstoppable(self,self.champion.skill.para[2])
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			#	目标死亡或无法选取则中断施法
			if self.champion.skill.para[6].flag.condition_flag.death_flag or self.champion.skill.para[6].flag.condition_flag.miss_flag[0]:
				self.champion.skill.para[0][0].value = 0
				self.champion.skill.continuous[3] = True
				self.condition.unstoppable.Clean(self.flag)
				print('%s持续施法期间目标%s死亡或不可选取，中断施法' %(self.champion.name,self.champion.skill.para[6].champion.name))
			else:
				end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
				# 施法结束
				if end_flag:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
					else:
						if self.champion.skill.para[1][0] != 2:
							self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][0] * self.enemy.champion.hp.max_value \
							*self.champion.attack_attribute.spell_power
						else:
							self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][1] * self.enemy.champion.hp.max_value \
							*self.champion.attack_attribute.spell_power
						# 伤害计算
						self.Spell_attack_damage_calculation()
						# 仅第一段伤害触发卢登
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack and self.champion.skill.para[1][0] == 0:
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						# 若第三段伤害造成伤害，则令敌人处于感电状态
						if self.champion.skill.para[1][0] == 2 and self.flag.damage_calculation_flag.spell_attack:
							if not self.enemy.flag.condition_flag.buff_invincible_flag:
								self.enemy.condition.electrification.Add_electrification(self.enemy,self.champion.skill.para[4])
					# 三段伤害计数
					self.champion.skill.para[1][0] += 1
		if self.champion.skill.para[1][0] >= self.champion.skill.para[1][1] or self.champion.skill.continuous[3]:
			self.champion.skill.para[1][0] = 0
			self.champion.skill.continuous[1] = False
			self.champion.skill.continuous[2] = True
			# 行为标志处理
			self.flag.move_flag.cast_spell = False
			self.move.current_move = 'normal_attack'
# 14-40厄斐琉斯
class Aphelios(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 40
		self.champion.name = 'Aphelios'
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 75
		self.champion.attack_attribute.attack_speed = 0.70
		self.champion.attack_attribute.AD = 43
		self.champion.attack_attribute.basic_AD = self.champion.attack_attribute.AD
		self.champion.defensive_attribute.armor = 22
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '银月'
		self.champion.relatedness.profession[0] = '枪手'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 4
		self.champion.skill.extra[2][2] = ['传知者与真知者', ['传知者与真知者：厄斐琉斯拥有5种皎','月武器，每次只装备主副两种武器，','并在子弹用完时自动切换，主动技能','根据施法时刻的主武器类型而定'], False]
		self.champion.skill.extra[2][3] = ['清辉夜凝',['清辉/夜凝：厄斐琉斯下一次普攻前会','用主副武器中非通碧者附加攻击带有','清辉标记的目标并移除清辉标记；带','有夜凝标记的目标会降低10%的攻速'], False]
		# 子弹数
		self.bullet_num = 6
		# 五种皎月武器以及相应技能
		self.moon_weapon = [['通碧',['通碧：使用通碧时额外提升8点AD，技','能触发通碧攻击时会给目标挂上清辉','标记','剩余子弹：%d' % self.bullet_num], \
		'月闪',['月闪：进行一次强化射击，对目标造','成85(+0.6*额外AD)点物理伤害，并将','其挂上标记：清辉']], \
		['断魄',['断魄：使用断魄时额外获得80%生命偷','取，并可以过量治疗，将额外治疗量','转化为护盾，持续10s','剩余子弹：%d' % self.bullet_num], \
		'对影',['对影：1.8s内交替用主、副武器共攻','击6下，伤害为正常普攻时的50%，对','影的攻击属于追加攻击：不会被闪避、','不计普攻次数、不触发分裂飓风效果']], \
		['坠明',['坠明：使用坠明攻击时会给敌人挂上','夜凝标记，带有夜凝标记的目标会降','低10%的攻速直到标记移除','剩余子弹：%d' % self.bullet_num], \
		'暗蚀',['暗蚀：移除所有敌人的夜凝标记，同','时使其眩晕2.8秒并造成90(+0.5*额外','AD)魔法伤害']], \
		['荧焰',['荧焰：使用荧焰时普攻变为范围魔法','伤害且不会被闪避，中心目标会受到','90%伤害，周围目标则受到45%伤害','剩余子弹：%d' % self.bullet_num], \
		'暝涌',['暝涌：向前方范围区域喷出一股火焰，','对命中的敌人造成60点魔法伤害，随','后用副武器攻击所有被暝涌命中的','敌人']], \
		['折镜',['折镜：普攻会追加飞轮攻击，每个造','成10(+0.3*额外AD)点物理伤害，技能','触发的折镜攻击每次生成一个飞轮','剩余子弹：%d；飞轮数：0' % self.bullet_num], \
		'驻灵',['驻灵：部署一个月之驻灵(上限3个)并','生成一个飞轮，月之驻灵会复制此刻','副武器的属性和60%伤害及厄斐琉斯此','时的攻速，持续9s']]]
		# 武器参数
		self.mwd_dic = {'通碧' : [self.bullet_num,False,[8,False]],'断魄' : [self.bullet_num,False,[0.8,10,False]],\
		'坠明' : [self.bullet_num,False,[0.10]],'荧焰' : [self.bullet_num,False,[0.9,0.45,False]],'折镜' : [self.bullet_num,False,[10,0.3,0]]}
		# 武器顺序
		self.weapon_seq = [0,1,2,3,4]
		# 每局随机打乱武器顺序
		shuffle(self.weapon_seq)
		# 初始主武器
		self.mwd_dic[self.moon_weapon[self.weapon_seq[0]][0]][1] = True
		self.Weapon_effect()
		self.champion.skill.name = self.moon_weapon[self.weapon_seq[0]][2]
		self.champion.skill.describe = self.moon_weapon[self.weapon_seq[0]][3]
		self.champion.skill.extra[2][0] = [self.moon_weapon[self.weapon_seq[0]][0], self.moon_weapon[self.weapon_seq[0]][1], False]
		self.champion.skill.extra[2][1] = [self.moon_weapon[self.weapon_seq[1]][0], self.moon_weapon[self.weapon_seq[1]][1], False]
		self.champion.skill.aoe[0] = True
		# 持续施法技能
		self.champion.skill.continuous[0] = True
		self.champion.skill.para = [[85,0.6],[[Time_count(),0.3],[0,6],1.8,0.5,0],[2.8,90,0.5],[60],[0.6,9,False]]
	
	# 武器效果处理
	def Weapon_effect(self):
		# 通碧加AD效果
		if self.mwd_dic['通碧'][1] and not self.mwd_dic['通碧'][2][1]:
			self.champion.attack_attribute.AD += self.mwd_dic['通碧'][2][0]
			self.mwd_dic['通碧'][2][1] = True
		elif not self.mwd_dic['通碧'][1] and self.mwd_dic['通碧'][2][1]:
			self.champion.attack_attribute.AD -= self.mwd_dic['通碧'][2][0]
			self.mwd_dic['通碧'][2][1] = False
		# 断魄加生命偷取效果
		if self.mwd_dic['断魄'][1] and not self.mwd_dic['断魄'][2][2]:
			self.champion.hemophagia += self.mwd_dic['断魄'][2][0]
			self.mwd_dic['断魄'][2][2] = True
		elif not self.mwd_dic['断魄'][1] and self.mwd_dic['断魄'][2][2]:
			self.champion.hemophagia -= self.mwd_dic['断魄'][2][0]
			self.mwd_dic['断魄'][2][2] = False
	# 计算主武器子弹，子弹为0时切换武器
	def Cal_bullet(self):
		self.mwd_dic[self.moon_weapon[self.weapon_seq[0]][0]][0] -= 1
		if self.mwd_dic[self.moon_weapon[self.weapon_seq[0]][0]][0] == 0:
			temp = self.weapon_seq[0]
			for i in range(4):
				self.weapon_seq[i] = self.weapon_seq[i+1]
			self.weapon_seq[4] = temp
			self.mwd_dic[self.moon_weapon[self.weapon_seq[4]][0]][0] = self.bullet_num
			self.mwd_dic[self.moon_weapon[self.weapon_seq[4]][0]][1] = False
			self.mwd_dic[self.moon_weapon[self.weapon_seq[0]][0]][1] = True
			# 重载技能
			self.champion.skill.name = self.moon_weapon[self.weapon_seq[0]][2]
			self.champion.skill.describe = self.moon_weapon[self.weapon_seq[0]][3]
			self.champion.skill.extra[2][0] = [self.moon_weapon[self.weapon_seq[0]][0], self.moon_weapon[self.weapon_seq[0]][1], False]
			self.champion.skill.extra[2][1] = [self.moon_weapon[self.weapon_seq[1]][0], self.moon_weapon[self.weapon_seq[1]][1], False]
			# 武器效果处理
			self.Weapon_effect()
			return True
		else:
			return False
	# 切换主副武器
	def Change_weapon(self):
		temp = self.weapon_seq[0]
		self.weapon_seq[0] = self.weapon_seq[1]
		self.mwd_dic[self.moon_weapon[self.weapon_seq[0]][0]][1] = True
		self.weapon_seq[1] = temp
		self.mwd_dic[self.moon_weapon[self.weapon_seq[1]][0]][1] = False
		# 重载技能
		self.champion.skill.name = self.moon_weapon[self.weapon_seq[0]][2]
		self.champion.skill.describe = self.moon_weapon[self.weapon_seq[0]][3]
		self.champion.skill.extra[2][0] = [self.moon_weapon[self.weapon_seq[0]][0], self.moon_weapon[self.weapon_seq[0]][1], False]
		self.champion.skill.extra[2][1] = [self.moon_weapon[self.weapon_seq[1]][0], self.moon_weapon[self.weapon_seq[1]][1], False]
		# 武器效果处理
		self.Weapon_effect()
	# 普攻主要部分
	def Normal_attack_main_part(self,dodge_flag):
		if self.mwd_dic['荧焰'][1]:
			# 荧焰普攻物理伤害转化为魔法伤害
			self.champion.attack_attribute.normal_attack.spell_damage = self.champion.attack_attribute.normal_attack.physical_damage \
			* self.champion.attack_attribute.spell_power
			self.champion.attack_attribute.normal_attack.physical_damage = 0
			# 显示效果
			self.enemy.flag.special_flag.effect['荧焰'][0] = True
		# 记录普攻伤害原值
		self.champion.attack_attribute.normal_attack_orig.physical_damage = self.champion.attack_attribute.normal_attack.physical_damage
		self.champion.attack_attribute.normal_attack_orig.spell_damage = self.champion.attack_attribute.normal_attack.spell_damage
		self.champion.attack_attribute.normal_attack_orig.real_damage = self.champion.attack_attribute.normal_attack.real_damage
		if not dodge_flag:
			# 计算伤害
			self.Normal_attack_damage_calculation()
			# 计算敌人回蓝
			self.champion.mp.MP_restore_2(self.flag, self, self.enemy, 1)
		if self.mwd_dic['荧焰'][1]:
			# 处理荧焰对周围敌人的溅射伤害，可触发攻击特效
			#	判断目标
			temp_enemy = self.enemy
			temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				# 复制伤害原值
				self.champion.attack_attribute.normal_attack.physical_damage = self.champion.attack_attribute.normal_attack_orig.physical_damage
				self.champion.attack_attribute.normal_attack.spell_damage = self.champion.attack_attribute.normal_attack_orig.spell_damage
				self.champion.attack_attribute.normal_attack.real_damage = self.champion.attack_attribute.normal_attack_orig.real_damage
				if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
				and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					# 显示效果
					self.enemy.flag.special_flag.effect['荧焰'][0] = True
					# 计算伤害
					self.Normal_attack_damage_calculation()
					# 计算敌人回蓝
					self.champion.mp.MP_restore_2(self.flag, self, self.enemy, 1)
			self.mwd_dic['荧焰'][2][2] = False
			self.enemy = temp_enemy
	# 普攻重载
	def Normal_attack(self):
		self.champion.attack_attribute.normal_attack_time_count += 1
		if self.champion.attack_attribute.normal_attack_time_count >= int((1 / self.champion.attack_attribute.attack_speed * 100) / time_correction[0]):
			# 普攻间隔时间计数值清零
			self.champion.attack_attribute.normal_attack_time_count = 0
			# 行动栏显示普攻
			if not self.flag.move_flag.show_normal_attack[0]:
				self.flag.move_flag.show_normal_attack[0] = True
				self.flag.move_flag.show_normal_attack[2] = 0
			else:
				# 刷新计时
				self.flag.move_flag.show_normal_attack[3].value = 0
				self.flag.move_flag.show_normal_attack[2] = 0
			# 普攻前处理清辉标记
			self.Qh()
			if self.flag.weapon_flag.krdd[0]:					# 触发狂热电刀效果
				self.weapon.Krdd(self) 
			if self.flag.weapon_flag.fljf[0]: 					# 触发分裂飓风效果
				self.flag.weapon_flag.fljf[2] = True
			# 枪手羁绊触发判断
			if self.flag.rela_flag['枪手'][0]:
				if (randint(0,99) < int(self.flag.rela_flag['枪手'][1][0] * 100)):
					self.flag.rela_flag['枪手'][4] = True
			# 敌人闪避判断
			dodge_flag = self.champion.defensive_attribute.dodge_mechanism.Dodge_judg(self.enemy) and (not self.enemy.flag.condition_flag.debuff_dizz_flag) and (not self.enemy.flag.condition_flag.debuff_frozen_flag)
			if self.flag.weapon_flag.jshp[0] or self.mwd_dic['荧焰'][1]:  					# 触发疾射火炮效果/荧焰普攻不会被闪避
				dodge_flag = False
			if dodge_flag:
				# 行动栏显示普攻被闪避
				self.flag.move_flag.show_normal_attack[2] = 2
				#self.champion.attack_attribute.normal_attack_damage.total_damage = 0
				if self.enemy.flag.weapon_flag.qfzl[0]: 			# 触发清风之灵效果(敌人)
					self.weapon.Qfzl(self)
				elif self.enemy.flag.weapon_flag.bmhs[0]:			# 触发冰脉护手效果(敌人)
					self.weapon.Bmhs(self)
			# 普攻主要部分
			self.Normal_attack_main_part(dodge_flag)
			# 剑士羁绊
			if self.flag.rela_flag['剑士'][0]:
				self.champion.relatedness.Swordsman(self)
			# 折镜飞轮追加攻击
			if self.flag.damage_calculation_flag.normal_attack and self.mwd_dic['折镜'][1] and self.mwd_dic['折镜'][2][2] > 0:
				self.Zj()
			# 触发鬼索之怒效果
			if self.flag.weapon_flag.gszn[0] and self.flag.damage_calculation_flag.normal_attack: 
				self.champion.attack_attribute.attack_speed *= (1 + self.flag.weapon_flag.gszn[1])
				self.flag.weapon_flag.gszn[2] += 1
			# 计算子弹
			self.Cal_bullet()
	# 追加攻击
	def Additional_attack(self):
		# 追加攻击伤害计算
		self.champion.attack_attribute.normal_attack.physical_damage = self.champion.attack_attribute.AD
		self.champion.attack_attribute.normal_attack.spell_damage = 0
		self.champion.attack_attribute.normal_attack.real_damage = 0
		if self.mwd_dic['通碧'][1]:
			self.Normal_attack_damage_calculation()
			# 计算敌人回蓝
			self.champion.mp.MP_restore_2(self.flag, self, self.enemy, 1)
			if self.flag.damage_calculation_flag.normal_attack:
				# 挂上清辉标记
				self.enemy.flag.special_flag.qh_sign = True
		elif self.mwd_dic['断魄'][1] or self.mwd_dic['坠明'][1]:
			self.Normal_attack_damage_calculation()
			# 计算敌人回蓝
			self.champion.mp.MP_restore_2(self.flag, self, self.enemy, 1)
		elif self.mwd_dic['荧焰'][1]:
			self.Normal_attack_main_part(False)
		elif self.mwd_dic['折镜'][1]:
			self.Normal_attack_damage_calculation()
			# 计算敌人回蓝
			self.champion.mp.MP_restore_2(self.flag, self, self.enemy, 1)
			# 折镜飞轮追加攻击
			if self.flag.damage_calculation_flag.normal_attack and self.mwd_dic['折镜'][2][2] > 0:
				self.Zj()
			# 增加飞轮
			self.mwd_dic['折镜'][2][2] += 1
	# 施放技能
	def Spell_attack(self):
		if not self.champion.skill.continuous[1]:
			if self.champion.skill.name == '对影':
				# 初始化
				self.champion.skill.para[1][0][0].value = 0
				self.champion.skill.para[1][1][0] = 0
				self.champion.skill.continuous[1] = True
				# 初始主武器编号记录
				self.champion.skill.para[1][4] = self.weapon_seq[0]
				self.flag.move_flag.show_cast_spell = [True,self.champion.skill.para[1][2],'对影']
				self.Special_spell_attack()
			elif self.champion.skill.name == '月闪':
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					extra_AD = self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD
					self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[0][0] + self.champion.skill.para[0][1] * extra_AD
					# 伤害计算
					self.Spell_attack_damage_calculation()
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
					# 挂上清辉标记
					if self.flag.damage_calculation_flag.spell_attack:
						self.enemy.flag.special_flag.qh_sign = True
			elif self.champion.skill.name == '暗蚀':
				temp_enemy = self.enemy
				for i in range(3):
					self.enemy = self.game.LR[~self.position+2][i]
					if self.enemy.flag.special_flag.yn_sign and not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
						# 移除夜凝标记、恢复攻速
						self.enemy.flag.special_flag.yn_sign = False
						if not self.enemy.flag.special_flag.Nabasre_flag:
							if self.enemy.champion.name == 'Jhin':
								self.enemy.As2cr(1 / (1 - self.mwd_dic['坠明'][2][0]))
							else:
								self.enemy.champion.attack_attribute.attack_speed /= (1 - self.mwd_dic['坠明'][2][0])
						# 计算伤害和眩晕效果
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:							# 处理魔法护盾
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果，只有此时的普攻目标出发伏击之爪的眩晕效果
							self.enemy.flag.weapon_flag.fjzz[1] = False
							if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag and self.enemy == temp_enemy:
								dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
								self.condition.dizz.Add_dizz(self,dizz_time)
						else:
							extra_AD = self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD
							self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[2][1] + self.champion.skill.para[2][2] * extra_AD)\
							 * self.champion.attack_attribute.spell_power
							# 伤害计算
							self.Spell_attack_damage_calculation()
							if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack and self.enemy == temp_enemy: # 触发卢登回声效果
								self.flag.weapon_flag.ldhs[1] = True
								self.flag.weapon_flag.ldhs[4] = self.enemy
							# 眩晕效果
							if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
								dizz_time = self.champion.skill.para[2][0] / self.enemy.champion.defensive_attribute.tenacity
								if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
									dizz_time += self.flag.weapon_flag.jdzc[1]
									self.flag.weapon_flag.jdzc[2] = True
									self.flag.weapon_flag.jdzc[3] += 1
								self.condition.dizz.Add_dizz(self.enemy,dizz_time)
				self.enemy = temp_enemy
			elif self.champion.skill.name == '暝涌':
				# 虽然是暝涌结束后再追加攻击，为了写代码方便，每攻击一个目标后直接追加攻击，两者效果是一样的
				# 处理敌人魔法护盾效果
				change_flag1 = False
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][0] * self.champion.attack_attribute.spell_power
					# 中心伤害计算
					self.Spell_attack_damage_calculation()
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
					# 追加攻击
					if self.flag.damage_calculation_flag.spell_attack:
						# 切换主副武器
						self.Change_weapon()
						# 追加攻击
						self.Additional_attack()
						# 计算子弹
						change_flag1 = self.Cal_bullet()
				# 周围伤害计算
				temp_enemy = self.enemy
				temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
				temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
				for i in range(2):
					if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
					and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
						self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						else:
							self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][0] * self.champion.attack_attribute.spell_power
							self.Spell_attack_damage_calculation()
							# 追加攻击
							if self.flag.damage_calculation_flag.spell_attack:
								if change_flag1:
									# 切换主副武器
									self.Change_weapon()
								# 追加攻击
								self.Additional_attack()
								# 计算子弹
								change_flag1 = self.Cal_bullet()
				if not change_flag1:
					# 切换主副武器
					self.Change_weapon()
				self.enemy = temp_enemy
				self.champion.skill.aoe[1] = False
			elif self.champion.skill.name == '驻灵':
				# 增加飞轮
				self.mwd_dic['折镜'][2][2] += 1
				# 部署月之驻灵
				pos_num = self.enemy.pos_num
				for i in range(3):
					if not moonbattery[pos_num].flag:
						moonbattery[pos_num].flag = True
						moonbattery[pos_num].position = self.position
						moonbattery[pos_num].Aphelios = self
						moonbattery[pos_num].weapon_num = self.weapon_seq[1]
						moonbattery[pos_num].attack_speed = self.champion.attack_attribute.attack_speed
						moonbattery[pos_num].time = self.champion.skill.para[4][1]
						moonbattery[pos_num].Init()
						break
					else:
						pos_num += 1
						if pos_num == 3:
							pos_num = 0
		if not self.champion.skill.continuous[1]:
			# 行为标志处理
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
			self.flag.move_flag.cast_spell = False
			self.Special_spell_attack()
			self.move.current_move = 'normal_attack'
		# 对影持续施法代码
		if self.champion.skill.continuous[1]:
			end_flag = self.champion.skill.para[1][0][0].Duration(self.champion.skill.para[1][0][1])
			# DOT结束
			if end_flag:
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					# 若此时的主武器编号与上一次的主武器编号相同则切换主副武器
					if self.weapon_seq[0] == self.champion.skill.para[1][4]:
						self.Change_weapon()
					# 追加攻击
					self.Additional_attack()
					# 记录主武器编号
					self.champion.skill.para[1][4] = self.weapon_seq[0]
					# 计算子弹
					self.Cal_bullet()
				# DOT计数
				self.champion.skill.para[1][1][0] += 1
				if self.champion.skill.para[1][1][0] == self.champion.skill.para[1][1][1]:
					self.champion.skill.para[1][1][0] = 0
					self.champion.skill.continuous[1] = False
					self.champion.skill.continuous[2] = True
					# 行为标志处理
					self.flag.move_flag.cast_spell = False
					self.move.current_move = 'normal_attack'
	# 处理清辉标记
	def Qh(self):
		temp_enemy = self.enemy
		for i in range(3):
			self.enemy = self.game.LR[~self.position+2][i]
			if self.enemy.flag.special_flag.qh_sign and not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
				if self.mwd_dic['通碧'][1]:
					# 切换主副武器
					self.Change_weapon()
					change_flag1 = True
				else:
					change_flag1 = False
				# 追加攻击：追加攻击不会被闪避、不计算普攻次数(故不触发电刀、羊刀)、且不触发飓风
				self.Additional_attack()
				# 显示效果
				self.champion.skill.extra[2][3][2] = True
				# 计算子弹
				change_flag2 = self.Cal_bullet()
				# 移除标记
				self.game.LR[~self.position+2][i].flag.special_flag.qh_sign = False
				if change_flag1 and not change_flag2:
					# 切换主副武器
					self.Change_weapon()
		self.enemy = temp_enemy
	# 对影伤害折算
	def Dy(self):
		self.champion.attack_attribute.normal_attack_damage.physical_damage *= self.champion.skill.para[1][3]
		self.champion.attack_attribute.normal_attack_damage.spell_damage *= self.champion.skill.para[1][3]
		self.champion.attack_attribute.normal_attack_damage.real_damage *= self.champion.skill.para[1][3]
	# 挂上夜凝标记
	def Yn(self):
		if not self.enemy.flag.special_flag.yn_sign:
			self.enemy.flag.special_flag.yn_sign = True
			if not self.enemy.flag.special_flag.Nabasre_flag:
				if self.enemy.champion.name == 'Jhin':
					self.enemy.As2cr(1 - self.mwd_dic['坠明'][2][0])
				else:
					self.enemy.champion.attack_attribute.attack_speed *= (1 - self.mwd_dic['坠明'][2][0])
	# 荧焰伤害折算
	def Yy(self):
		# 中心目标
		if not self.mwd_dic['荧焰'][2][2]:
			self.champion.attack_attribute.normal_attack_damage.physical_damage *= self.mwd_dic['荧焰'][2][0]
			self.champion.attack_attribute.normal_attack_damage.spell_damage *= self.mwd_dic['荧焰'][2][0]
			self.champion.attack_attribute.normal_attack_damage.real_damage *= self.mwd_dic['荧焰'][2][0]
			self.mwd_dic['荧焰'][2][2] = True
		# 周围目标
		else:
			self.champion.attack_attribute.normal_attack_damage.physical_damage *= self.mwd_dic['荧焰'][2][1]
			self.champion.attack_attribute.normal_attack_damage.spell_damage *= self.mwd_dic['荧焰'][2][1]
			self.champion.attack_attribute.normal_attack_damage.real_damage *= self.mwd_dic['荧焰'][2][1]
	# 折镜飞轮攻击
	def Zj(self):
		extra_AD = self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD
		# 幻影之舞免疫穿甲
		if self.enemy.flag.weapon_flag.hyzw[0]:
			armor_penetration = 0
		else:
			armor_penetration = self.champion.attack_attribute.armor_penetration
		# 暴击判断
		if self.champion.attack_attribute.crit_mechanism.crit_flag:
			crit_multiple = self.champion.attack_attribute.crit_mechanism.crit_multiple
		else:
			crit_multiple = 1
		damage = (self.mwd_dic['折镜'][2][0] + self.mwd_dic['折镜'][2][1] * extra_AD) \
		* (100 / (100 + (self.enemy.champion.defensive_attribute.armor * (1 - armor_penetration/100)))) * crit_multiple \
		* self.enemy.condition.matigation.value
		for i in range(self.mwd_dic['折镜'][2][2]):
			# 扣血、击杀判断
			self.enemy.champion.hp.HP_reduce(damage,self,self.enemy)
			# 触发雷霆羁绊
			if self.flag.rela_flag['雷霆'][0]:
				self.champion.relatedness.Thunder(self)
			# 累计造成伤害
			self.champion.attack_attribute.all_damage.physical_damage += damage
			#print('飞轮造成物理伤害：%.2f' % damage)
			self.champion.attack_attribute.all_damage.Total_damage_calculation()
		# 显示效果
		self.enemy.flag.special_flag.effect['飞轮'][0] = True
	# 驻灵伤害折算
	def Zl(self):
		self.champion.attack_attribute.normal_attack_damage.physical_damage *= self.champion.skill.para[4][0]
		self.champion.attack_attribute.normal_attack_damage.spell_damage *= self.champion.skill.para[4][0]
		self.champion.attack_attribute.normal_attack_damage.real_damage *= self.champion.skill.para[4][0]
	# 特殊死亡处理
	def Death_deal_other(self):
		for i in range(3):
			moonbattery[i].flag = False
# 15-41格雷福斯
class Graves(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 41
		self.champion.name = 'Graves'
		self.champion.skill.name = '大号铅弹'
		self.champion.skill.describe = ['大号铅弹：格雷福斯的散弹枪在普攻','时会对前方敌人进行范围攻击，中心','目标受到90%普攻伤害，周围目标受到','65%普攻伤害']
		self.champion.skill.active_skill = False
		self.champion.hp.max_value = 890
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 0
		self.champion.mp.max_value = 0
		self.champion.attack_attribute.attack_speed = 0.68
		self.champion.attack_attribute.AD = 48
		self.champion.defensive_attribute.armor = 35
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '钢铁'
		self.champion.relatedness.profession[0] = '枪手'
		# 格雷福斯被动借用狂战士羁绊的代码
		self.flag.rela_flag['狂战士'][0] = True
		self.champion.skill.para = [0.9,0.65,[False]]
	
	def Spell_attack(self):
		pass
	# 普攻前特殊效果
	def Special_normal_attack(self):
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.show_cast_spell[1] = 0.4
# 16-42亚索
class Yasuo(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 42
		self.champion.name = 'Yasuo'
		self.skill = [['斩钢闪',['斩钢闪：亚索向前出剑，对目标造成','20(+1.0*AD)物理伤害，且计算为普','攻伤害；两次斩钢闪后，下一次技能','变为旋风烈斩']],\
		['旋风烈斩',['旋风烈斩：亚索用剑气形成一阵能够','击飞敌人的飓风，对目标造成120点魔','法伤害并眩晕2.5s；下一次技能变为','斩钢闪']]]
		self.champion.skill.name = self.skill[0][0]
		self.champion.skill.describe = self.skill[0][1]
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 0
		self.champion.mp.max_value = 55
		self.champion.attack_attribute.attack_speed = 0.66
		self.champion.attack_attribute.AD = 45
		self.champion.defensive_attribute.armor = 30
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '云霄' if version[0] == 2 else '奥德赛'
		self.champion.relatedness.profession[0] = '剑士'
		if version[0] == 2:
			self.champion.skill.extra[0] = True
			self.champion.skill.extra[1] = 1
			self.champion.skill.extra[2][0] = ['风之障壁',['风之障壁：亚索在开局时拥有150点护','盾值，持续5s，并在周围队友死去时','再次刷新','彩蛋：亚索触发被动时会快乐亮牌'],False]

		self.champion.skill.para = [0,[20,1],[120,2.5],[150,5,False,False],[False,1,Time_count(),0.1]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 斩钢闪
		if self.champion.skill.name == '斩钢闪':
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			# 触发敌人伏击之爪效果
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				# 普攻伤害初始化
				self.champion.attack_attribute.normal_attack.__init__(self.champion.attack_attribute.AD)
				# 普攻伤害
				self.champion.attack_attribute.normal_attack.physical_damage = self.champion.skill.para[1][0] + self.champion.skill.para[1][1] * \
				self.champion.attack_attribute.AD
				# 计数溢出，则迅速进行下一次普攻
				self.champion.attack_attribute.normal_attack_time_count = 1000
				self.Normal_attack()
				# 计算回蓝
				self.champion.mp.MP_restore_1(self.flag, self, self.enemy)
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.normal_attack:
					self.champion.relatedness.Blast(self)
			self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
			# 切换技能
			self.champion.skill.para[0] += 1
			if self.champion.skill.para[0] == 2:
				self.champion.skill.name = self.skill[1][0]
				self.champion.skill.describe = self.skill[1][1]
		# 旋风烈斩
		elif self.champion.skill.name == '旋风烈斩':
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			# 触发敌人伏击之爪效果
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
						dizz_time += self.flag.weapon_flag.jdzc[1]
						self.flag.weapon_flag.jdzc[2] = True
						self.flag.weapon_flag.jdzc[3] += 1
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[2][0] * self.champion.attack_attribute.spell_power
				# 伤害计算
				self.Spell_attack_damage_calculation()
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 眩晕效果
				if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
					dizz_time = self.champion.skill.para[2][1] / self.enemy.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self.enemy,dizz_time)
					# 触发爆破炸弹效果
					if self.flag.weapon_flag.bpzd[0] and not self.flag.rela_flag['爆破专家'][0]:
						self.weapon.Bpzd(self,self.enemy)
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
					self.champion.relatedness.Blast(self)
			self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
			# 切换技能
			self.champion.skill.name = self.skill[0][0]
			self.champion.skill.describe = self.skill[0][1]
			self.champion.skill.para[0] = 0
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 风之障壁
	def Special_effect_deal(self):
		if version[0] == 2:
			# 判断周围队友生存情况
			numTF = [self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
			num_pos = [self.pos_num - 1, self.pos_num + 1]
			death_flag = [True,True]
			for i in range(2):
				if numTF[i]:
					if not self.game.LR[self.position][num_pos[i]].flag.condition_flag.death_flag:
						death_flag[i] = False
			shield_flag = death_flag[0] and death_flag[1]
			shield = [(not self.champion.skill.para[3][2]),(not self.champion.skill.para[3][3] and shield_flag)]
			for i in range(2):
				if shield[i]:
					shield_add = self.champion.skill.para[3][0] * self.champion.attack_attribute.spell_power
					self.condition.shield.Add_shield(self,shield_add,self.champion.skill.para[3][1])
					if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
						self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
						self.flag.weapon_flag.crxl[3] = True
					self.champion.skill.para[3][2+i] = True
					self.champion.skill.extra[2][0][2] = True
					# 亮牌彩蛋
					if version[0] == 2:
						self.champion.skill.para[4][0] = True
# 17-43布里兹
class Blitz(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 43
		self.champion.name = 'Blitz'
		self.champion.skill.name = '静电力场'
		self.champion.skill.describe = ['静电力场：布里兹释放静电力场，摧','毁范围内敌人的护盾并造成60点魔法','伤害和1.5s的沉默效果']
		self.champion.hp.max_value = 970
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 100
		self.champion.attack_attribute.attack_speed = 0.56
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 38
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '钢铁'
		self.champion.relatedness.profession[0] = '斗士'
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['能量屏障',['能量屏障：布里兹生命低于20%时，产','生(0.3*最大生命值)护盾值，持续8s','未触发'],False]

		self.champion.skill.para = [60,1.5,[False,0.2,0.3,8]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			# 破盾
			if self.enemy.condition.shield.value > 0 and not self.enemy.flag.condition_flag.buff_invincible_flag:
				self.enemy.condition.shield.value = 0
				print('布里兹触发破盾机制！')
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 沉默
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.special_flag.chakra_flag:
				self.condition.silence.Add_silence(self.enemy,self.champion.skill.para[1])
		# 周围伤害计算
		temp_enemy = self.enemy
		temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
		temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
		for i in range(2):
			if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
			and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
				self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
					# 破盾
					if self.enemy.condition.shield.value > 0 and not self.enemy.flag.condition_flag.buff_invincible_flag:
						self.enemy.condition.shield.value = 0
						print('布里兹触发破盾机制！')
					self.Spell_attack_damage_calculation()
					# 沉默
					if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.special_flag.chakra_flag:
						self.condition.silence.Add_silence(self.enemy,self.champion.skill.para[1])
		self.enemy = temp_enemy
		self.champion.skill.aoe[1] = False
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 法力屏障
	def Barrier(self):
		# 获得护盾
		shield_add = self.champion.skill.para[2][2] * self.champion.hp.max_value * self.champion.attack_attribute.spell_power
		self.condition.shield.Add_shield(self,shield_add,self.champion.skill.para[2][3])
		if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
			self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
			self.flag.weapon_flag.crxl[3] = True
		self.champion.skill.extra[2][0][2] = True	
		self.champion.skill.para[2][0] = True
# 18-44易
class Yi(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 44
		self.champion.name = 'Yi'
		self.champion.skill.name = '冥想'
		self.champion.skill.describe = ['冥想：易开始冥想，在2s内减免60%伤','害且每0.4s回复15生命值(每失去1%生','命值，治疗效果提升1%)，冥想结束后','的6s内普攻附带40点额外魔法伤害']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.70
		self.champion.attack_attribute.AD = 47
		self.champion.defensive_attribute.armor = 26
		self.champion.defensive_attribute.spell_resistance = 21
		self.champion.relatedness.element[0] = '影' if version[0] == 2 else '星神'
		self.champion.relatedness.profession[0] = '剑士'
		# 持续施法技能
		self.champion.skill.continuous[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 2
		self.champion.skill.extra[2][0] = ['双重打击',['双重打击：易的每第四次连续普攻将','进行双重打击，第二次攻击造成110%','伤害且不消耗剑士羁绊效果','连续普攻计数：0'],False]
		self.champion.skill.extra[2][1] = ['高原血统',['高原血统：易不受减攻速效果影响'],False]
		# 不受减攻速效果影响标志
		self.flag.special_flag.Nabasre_flag = True
		self.champion.skill.para = [[Time_count(),0.4,0,5],2,0.6,15,[False,Time_count(),6,40,False],[False,1.1]]

	# 使用技能（施法）
	def Spell_attack(self):
		numTF = [True, self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
		num_pos = [self.pos_num, self.pos_num - 1, self.pos_num +1]
		# 开始施法
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[0][0].value = 0
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = True
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[1]
			# 减伤效果
			matigation_value = 1 - self.champion.skill.para[2]
			self.condition.matigation.Add_matigation(self,matigation_value,self.champion.skill.para[1])
			# 星之守护者羁绊效果
			if self.flag.rela_flag['星之守护者'][0]:
				self.champion.relatedness.Star(self)
			# 魅惑挂坠效果
			if self.flag.weapon_flag.mhgz[0]:
				self.weapon.Mhgz(self)
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			if self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1]):
				# 回血DOT
				hp_restore_value = self.champion.skill.para[3] * (1 + (self.champion.hp.max_value - self.champion.hp.value) / self.champion.hp.max_value) \
				* self.champion.attack_attribute.spell_power
				self.champion.hp.HP_restore(hp_restore_value, self.champion, self)
				if self.flag.weapon_flag.crxl[0]: 										# 触发炽热香炉效果
					self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
					self.flag.weapon_flag.crxl[3] = True
				self.champion.skill.para[0][2] += 1
		if self.champion.skill.para[0][2] >= self.champion.skill.para[0][3]:
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = False
			self.champion.skill.continuous[2] = True
			# 施法结束时重置连续普攻计数
			self.champion.attack_attribute.attack_count = 0
			# 冥想结束后一段时间内普攻附带额外魔法伤害，若冥想被打断则没有该效果
			self.champion.skill.para[4][0] = True
			# 行为标志处理
			self.flag.move_flag.cast_spell = False
			self.move.current_move = 'normal_attack'	
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 冥想结束后计时
		if self.champion.skill.para[4][0]:
			if self.champion.skill.para[4][1].Duration(self.champion.skill.para[4][2]):
				self.champion.skill.para[4][0] = False
				self.champion.skill.para[4][4] = False
		# 受到控制效果时普攻计数重置
		if self.flag.condition_flag.debuff_disarm_flag or self.flag.condition_flag.debuff_frozen_flag or self.flag.condition_flag.debuff_dizz_flag \
		or self.flag.condition_flag.suppress[0] or self.flag.condition_flag.debuff_taunt_flag:
			self.champion.attack_attribute.attack_count = 0
	# 普攻前特殊效果
	def Special_normal_attack(self):
		# 计算额外魔法伤害
		if self.champion.skill.para[4][0]:
			self.champion.attack_attribute.normal_attack.spell_damage += self.champion.skill.para[4][3] * self.champion.attack_attribute.spell_power
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		# 易转爆破专家时，冥想后的第一下普攻触发爆破专家羁绊效果
		if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.normal_attack and self.champion.skill.para[4][0]\
		 and not self.champion.skill.para[4][4]:
			self.champion.relatedness.Blast(self)
			self.champion.skill.para[4][4] = True
		# 双重打击，双重打击本身不计算连续攻击数
		if not self.champion.skill.para[5][0]:
			self.champion.attack_attribute.attack_count += 1
		if self.champion.attack_attribute.attack_count == 4:
			self.champion.attack_attribute.attack_count = 0
			# 计数溢出，则迅速进行下一次普攻
			self.champion.attack_attribute.normal_attack_time_count = 1000
			self.champion.skill.para[5][0] = True
			# 普攻伤害初始化
			self.champion.attack_attribute.normal_attack.__init__(self.champion.attack_attribute.AD)
			self.Normal_attack()
			# 计算回蓝
			self.champion.mp.MP_restore_1(self.flag, self, self.enemy)
			self.champion.skill.para[5][0] = False
			# 显示
			self.champion.skill.extra[2][0][2] = True
# 19-45慎
class Shen(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 45
		self.champion.name = 'Shen'
		self.champion.skill.name = '奥义！魂佑'
		self.champion.skill.describe = ['奥义！魂佑：慎的魂刃会创建一个持','续3s的防御结界，使自己和周围的','队友处于完全闪避状态']
		self.champion.hp.max_value = 910
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.68
		self.champion.attack_attribute.AD = 46
		self.champion.defensive_attribute.armor = 36
		self.champion.defensive_attribute.spell_resistance = 26
		self.champion.relatedness.element[0] = '极地' if version[0] == 2 else '未来战士'
		self.champion.relatedness.profession[0] = '忍剑士' if version[0] == 2 else '剑士'
		if version[0] == 2:
			self.flag.special_flag.chakra_flag = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['忍法！气合盾',['忍法！气合盾：慎每次触发闪避时，','获得30点护盾值，持续6s','触发次数：0'],False]
		self.champion.skill.para = [[False,Time_count(),3],[30,5,0]]

	# 使用技能（施法）
	def Spell_attack(self):
		self.champion.skill.para[0][0] = True
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[0][2]
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 完全闪避
		if self.champion.skill.para[0][0]:
			end_flag = self.champion.skill.para[0][1].Duration(self.champion.skill.para[0][2])
			if end_flag:
				# 退出完全闪避
				for i in range(3):
					if self.friend[i].champion.defensive_attribute.dodge_mechanism.all_dodge[2]:
						self.friend[i].champion.defensive_attribute.dodge_mechanism.all_dodge[2] = False
				self.champion.skill.para[0][0] = False
			else:
				# 完全闪避
				numTF = [True,self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
				num_pos = [self.pos_num,self.pos_num - 1, self.pos_num +1]
				for i in range(3):
					if numTF[i]:
						if not self.game.LR[self.position][num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[self.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
							self.game.LR[self.position][num_pos[i]].champion.defensive_attribute.dodge_mechanism.all_dodge[2] = True				
	# 忍法!气合盾
	def Ninja_shield(self):
		# 获得护盾
		shield_add = self.champion.skill.para[1][0] * self.champion.attack_attribute.spell_power
		self.condition.shield.Add_shield(self,shield_add,self.champion.skill.para[1][1])
		if self.flag.weapon_flag.crxl[0]: 													# 触发炽热香炉效果
			self.condition.fervor.Add_fervor(self,self.flag.weapon_flag.crxl[2][2])
			self.flag.weapon_flag.crxl[3] = True
		self.champion.skill.extra[2][0][2] = True	
		self.champion.skill.para[1][2] += 1
	# 特殊死亡处理
	def Death_deal_other(self):
		if self.champion.skill.para[0][0]:
			for i in range(3):
				self.game.LR[self.position][i].champion.defensive_attribute.dodge_mechanism.all_dodge[2] = False
			self.champion.skill.para[0][0] = False
# 20-46阿卡丽
class Akali(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 46
		self.champion.name = 'Akali'
		self.skill = [['我流秘奥义！表里杀缭乱',['我流秘奥义！表里杀缭乱：阿卡丽向','最远敌人突刺，对途径敌人造成50点','物理伤害并眩晕0.3s，在之后的2s内','未受到控制效果则可进行第二段突刺']],\
		['我流秘奥义！表里杀缭乱2',['我流秘奥义！表里杀缭乱：阿卡丽向','最远敌人进行第二段突刺，对途径敌','人基于敌人已损失生命值造成80~180','的魔法伤害']]]
		self.champion.skill.name = self.skill[0][0]
		self.champion.skill.describe = self.skill[0][1]
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 70
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.64
		self.champion.attack_attribute.AD = 39
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '银月'
		self.champion.relatedness.profession[0] = '忍者'
		self.flag.special_flag.chakra_flag = True
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['我流忍法！潜龙印',['我流忍法！潜龙印：阿卡丽切换攻击','目标后的下次普攻附带35点魔法伤害，','并使目标重伤5s','触发次数：0'],False]
		self.champion.skill.para = [[False,False],[50,0.3],[False,Time_count(),3],[80,180],[None,35,False,5,0]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 第一段突刺
		self.Assassinate(1)
		self.champion.skill.aoe[1] = False
		# 卢登标志重置
		self.champion.skill.para[0][1] = False
		self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
		# 判断有无被中断
		if not self.champion.skill.para[0][0]:
			self.champion.skill.name = self.skill[1][0]
			self.champion.skill.describe = self.skill[1][1]
			self.champion.skill.para[2][0] = True
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 突刺伤害处理
	def Spell_damage_deal(self,mode,pos_num):
		# 判断有无被中断
		if not self.champion.skill.para[0][0]:
			if not self.game.LR[~self.position+2][pos_num].flag.condition_flag.death_flag \
			and not  self.game.LR[~self.position+2][pos_num].flag.condition_flag.miss_flag[0]:
				self.enemy = self.game.LR[~self.position+2][pos_num]
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
						# 被中断
						self.champion.skill.para[0][0] = True
						print('Akali%d段突刺被中断' % mode)
				else:
					# 第一段突刺
					if mode == 1:
						self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[1][0]
						# 伤害计算
						self.Spell_attack_damage_calculation()
						# 触发卢登回声效果，仅第一个目标触发
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack and not self.champion.skill.para[0][1]: 
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
							self.champion.skill.para[0][1] = True
						# 眩晕
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.champion.skill.para[1][1] / self.enemy.champion.defensive_attribute.tenacity
							if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
								dizz_time += self.flag.weapon_flag.jdzc[1]
								self.flag.weapon_flag.jdzc[2] = True
								self.flag.weapon_flag.jdzc[3] += 1
							self.condition.dizz.Add_dizz(self.enemy,dizz_time)
					# 第二段突刺
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][0] + (self.champion.skill.para[3][1] - self.champion.skill.para[3][0])\
						 * ((self.enemy.champion.hp.max_value - self.enemy.champion.hp.value) / self.enemy.champion.hp.max_value)
						# 伤害计算
						self.Spell_attack_damage_calculation()
						# 触发卢登回声效果，仅第一个目标触发
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack and not self.champion.skill.para[0][1]: 
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
							self.champion.skill.para[0][1] = True
	# 突刺
	def Assassinate(self,mode):
		#	判断目标
		if self.enemy.pos_num == 0:
			self.Spell_damage_deal(mode,0)
			self.Spell_damage_deal(mode,1)
			self.Spell_damage_deal(mode,2)
		elif self.enemy.pos_num == 2:
			self.Spell_damage_deal(mode,2)
			self.Spell_damage_deal(mode,1)
			self.Spell_damage_deal(mode,0)
		else:
			self.Spell_damage_deal(mode,1)
			p = [0,2]
			self.Spell_damage_deal(mode,p[randint(0,1)])	
	# 技能特殊效果处理
	def Special_effect_deal(self):
		# 二段突刺前计时
		if self.champion.skill.para[2][0]:
			end_flag = self.champion.skill.para[2][1].Duration(self.champion.skill.para[2][2])
			if end_flag:
				self.champion.skill.para[2][0] = False
				# 二段突刺
				self.Assassinate(2)
				# 重置普攻
				self.champion.attack_attribute.normal_attack_time_count = 0
				# 标志位重置
				self.champion.skill.para[2][0] = False
				self.champion.skill.aoe[1] = False
				# 卢登标志重置
				self.champion.skill.para[0][1] = False
				self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
				self.champion.skill.name = self.skill[0][0]
				self.champion.skill.describe = self.skill[0][1]
				self.flag.move_flag.show_cast_spell[0] = True
			else:
				# 判断有无被控制效果中断(不考虑缴械状态)
				if self.flag.condition_flag.debuff_dizz_flag or self.flag.condition_flag.debuff_frozen_flag\
				 or self.flag.condition_flag.suppress[0] or self.flag.condition_flag.debuff_taunt_flag:
					self.champion.skill.para[2][0] = False
					print('Akali突刺间隔中被打断')
					self.champion.skill.para[2][1].value = 0
					self.champion.skill.name = self.skill[0][0]
					self.champion.skill.describe = self.skill[0][1]	
	# 普攻前特殊效果
	def Special_normal_attack(self):
		# 判断目标有无变换
		if self.enemy != self.champion.skill.para[4][0]:
			# 第一次不计算
			if self.champion.skill.para[4][0] != None:
				# 附加额外魔法伤害
				self.champion.attack_attribute.normal_attack.spell_damage += (self.champion.skill.para[4][1] * self.champion.attack_attribute.spell_power)
				self.champion.skill.para[4][2] = True
			self.champion.skill.para[4][0] = self.enemy
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		if self.champion.skill.para[4][2]:
			if self.flag.damage_calculation_flag.normal_attack:
				# 潜龙印重伤效果
				self.condition.injury.Add_injury(self.enemy, self.champion.skill.para[4][3]) 
			self.champion.skill.extra[2][0][2] = True
			self.champion.skill.para[4][4] += 1
			self.champion.skill.para[4][2] = False
# 21-47凯南
class Kennen(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 47
		self.champion.name = 'Kennen'
		self.champion.skill.name = '秘奥义！万雷天牢引'
		self.champion.skill.describe = ['秘奥义！万雷天牢引：凯南在周围召','唤天雷风暴(持续4.8s)，每0.8s对敌','人造成50点魔法伤害并叠加一层雷缚','印标记，但期间自己不能普攻']
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.64
		self.champion.attack_attribute.AD = 39
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '雷霆'
		self.champion.relatedness.profession[0] = '忍者'
		self.flag.special_flag.chakra_flag = True
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['忍法！雷缚印',['忍法！雷缚印：凯南的技能与雷霆羁','绊引起的落雷会给目标叠加1层雷缚印','标记，达到3层时会眩晕目标1.5s','触发次数：0'],False]

		self.champion.skill.para = [False,[Time_count(),0.8,4.8],[0,6],50,1.5,0]

	# 使用技能（施法）
	def Spell_attack(self):
		# 天雷标志
		if not self.champion.skill.para[0]:
			self.champion.skill.para[0] = True
			self.flag.special_flag.thunderbolt = True
			# 缴械自己
			self.condition.disarm.Add_disarm(self,self.champion.skill.para[1][2])
		else:# 重置时间
			self.champion.skill.para[1][0].value = 0
			self.champion.skill.para[2][0] = 0
		# 行为标志处理
		self.flag.move_flag.show_cast_spell = [True,self.champion.skill.para[2][1]]
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if self.champion.skill.para[0]:
			end_flag = self.champion.skill.para[1][0].Duration(self.champion.skill.para[1][1])
			if end_flag:
				# 计算伤害
				if not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.attack_attribute.spell_power
						# 中心伤害计算
						self.Spell_attack_damage_calculation()
						# 显示
						self.enemy.flag.special_flag.effect['天雷'][0] = True
						self.Thunder_sign(self.enemy)
						# 仅第一段伤害触发卢登回声效果
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack and self.champion.skill.para[2][0] == 0: 
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
					# 周围伤害计算
					temp_enemy = self.enemy
					temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
					temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.attack_attribute.spell_power
					for i in range(2):
						if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
						and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
							self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
							# 处理敌人魔法护盾效果
							if self.enemy.flag.condition_flag.buff_magic_shield_flag:
								self.enemy.condition.magic_shield.Clean(self.enemy.flag)
							else:
								self.Spell_attack_damage_calculation()
								# 显示
								self.enemy.flag.special_flag.effect['天雷'][0] = True
								self.Thunder_sign(self.enemy)
					self.enemy = temp_enemy
					self.champion.skill.aoe[1] = False	
				# DOT计数
				self.champion.skill.para[2][0] += 1
				if self.champion.skill.para[2][0] == self.champion.skill.para[2][1]:
					self.champion.skill.para[2][0] = 0
					self.champion.skill.para[0] = False
					self.flag.special_flag.thunderbolt = False
	# 雷缚印
	def Thunder_sign(self,enemy):
		if enemy.flag.special_flag.thunder_sign < 3:
			enemy.flag.special_flag.thunder_sign += 1
		if enemy.flag.special_flag.thunder_sign == 3:
			# 眩晕
			if not enemy.flag.condition_flag.buff_invincible_flag and not enemy.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.champion.skill.para[4] / enemy.champion.defensive_attribute.tenacity
				if self.flag.weapon_flag.jdzc[0]: 											# 触发极地战锤效果
					dizz_time += self.flag.weapon_flag.jdzc[1]
					self.flag.weapon_flag.jdzc[2] = True
					self.flag.weapon_flag.jdzc[3] += 1
				self.condition.dizz.Add_dizz(enemy,dizz_time)
			self.champion.skill.para[5] += 1
# 22-48加里奥
class Galio(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 48
		self.champion.name = 'Galio'
		self.champion.skill.name = '杜朗护盾'
		self.champion.skill.describe = ['杜朗护盾：加里奥获得70%减伤并嘲讽','周围敌人5s强制其普攻加里奥，并造','成30(+0.3*额外魔抗)点魔法伤害，结','束嘲讽后敌人会重新攻击原先的目标']
		self.champion.hp.max_value = 1050
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.56
		self.champion.attack_attribute.AD = 42
		self.champion.defensive_attribute.armor = 40
		self.champion.defensive_attribute.basic_armor = self.champion.defensive_attribute.armor
		self.champion.defensive_attribute.spell_resistance = 35
		self.champion.defensive_attribute.basic_spell_resistance = self.champion.defensive_attribute.spell_resistance
		self.champion.relatedness.element[0] = '钢铁'
		self.champion.relatedness.profession[0] = '守护神'
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['巨像重击',['巨像重击：加里奥每受到8次攻击，就','会强化下一次的普攻，使其额外造成','35(+0.3*额外护甲)的范围魔法伤害','触发次数：0'],False]

		self.champion.skill.para = [0.70,5,[30,0.3],[0,8,False],[35,0.3],0]
	
	# 使用技能（施法）
	def Spell_attack(self):
		# 减伤效果
		matigation_value = 1 - self.champion.skill.para[0]
		self.condition.matigation.Add_matigation(self,matigation_value,self.champion.skill.para[1])
		# 嘲讽效果和伤害计算
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			extra_spell_resistance = self.champion.defensive_attribute.spell_resistance - self.champion.defensive_attribute.basic_spell_resistance
			self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[2][0] + self.champion.skill.para[2][1] \
				* extra_spell_resistance) * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 嘲讽
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
				taunt_time = self.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
				self.condition.taunt.Add_taunt(self.enemy,taunt_time,self)
		# 周围伤害计算
		temp_enemy = self.enemy
		temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
		temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
		for i in range(2):
			if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
			and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
				self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				else:
					extra_spell_resistance = self.champion.defensive_attribute.spell_resistance - self.champion.defensive_attribute.basic_spell_resistance
					self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[2][0] + self.champion.skill.para[2][1] \
						* extra_spell_resistance) * self.champion.attack_attribute.spell_power
					self.Spell_attack_damage_calculation()
					# 嘲讽
					if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
						taunt_time = self.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
						self.condition.taunt.Add_taunt(self.enemy,taunt_time,self)
		self.enemy = temp_enemy
		self.champion.skill.aoe[1] = False
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 巨像重击
	def Thump(self):
		if self.champion.skill.para[3][0] < self.champion.skill.para[3][1]:
			self.champion.skill.para[3][0] += 1
			if self.champion.skill.para[3][0] == self.champion.skill.para[3][1]:
				self.champion.skill.para[3][2] = True
				self.champion.skill.extra[2][0][2] = True
	# 普攻前特殊效果：巨像重击(不触发卢登、伏击之爪、魔法护盾)
	def Special_normal_attack(self):
		if self.champion.skill.para[3][2]:
			extra_armor = self.champion.defensive_attribute.armor - self.champion.defensive_attribute.basic_armor
			# 附加额外魔法伤害
			self.champion.attack_attribute.normal_attack.spell_damage += ((self.champion.skill.para[4][0] + self.champion.skill.para[4][1] * extra_armor) * self.champion.attack_attribute.spell_power)
	# 普攻后特殊效果：巨像重击(可触发死亡秘典、珠光拳套)
	def Special_normal_attack2(self):
		if self.champion.skill.para[3][2]:
			# 周围伤害计算
			temp_enemy = self.enemy
			temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
				and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					extra_armor = self.champion.defensive_attribute.armor - self.champion.defensive_attribute.basic_armor
					# 额外魔法伤害
					self.champion.attack_attribute.spell_attack.spell_damage += ((self.champion.skill.para[4][0] + self.champion.skill.para[4][1] * extra_armor) * self.champion.attack_attribute.spell_power)
					self.Spell_attack_damage_calculation()
			self.enemy = temp_enemy
			self.champion.skill.aoe[1] = False
			self.champion.skill.para[5] += 1
			# 重置巨像重击
			self.champion.skill.para[3][2] = False
			self.champion.skill.extra[2][0][2] = False
			self.champion.skill.para[3][0] = 0
# 23-49烬
class Jhin(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 49
		self.champion.name = 'Jhin'
		self.champion.skill.name = '低语'
		self.champion.skill.describe = ['低语：低语的四发子弹发射完毕后需','1.5s装弹；最后一发必定暴击，附加','目标28%已损失生命的物理伤害(最低','100)；烬每1%的额外攻速转化为0.8AD']
		self.champion.skill.active_skill = False
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 0
		self.champion.mp.max_value = 0
		self.champion.attack_attribute.attack_speed = 0.69
		self.attack_speed_temp = self.champion.attack_attribute.attack_speed
		self.champion.attack_attribute.AD = 55
		self.champion.attack_attribute.basic_AD = self.champion.attack_attribute.AD
		self.champion.defensive_attribute.armor = 24
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '影' if version[0] == 2 else '暗星'
		self.champion.relatedness.profession[0] = '枪手'

		self.champion.attack_attribute.attack_count = 0                      		# 攻击计数值
		self.champion.skill.para = [[False,Time_count(),1.5],[False,0.28,0.8,100]]

	# 使用技能（施法）
	def Spell_attack(self):
		pass
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if self.champion.skill.para[0][0]:
			end_flag = self.champion.skill.para[0][1].Duration(self.champion.skill.para[0][2])
			if end_flag:
				self.champion.attack_attribute.attack_count = 0
				self.champion.skill.para[0][0] = False
				self.move.current_move = 'normal_attack'
			else:
				self.move.current_move = 'load'
	# 普攻前特殊效果
	def Special_normal_attack(self):
		if not self.champion.skill.para[0][0]:
			self.champion.skill.para[1][0] = False
			self.champion.attack_attribute.attack_count += 1
			if self.champion.attack_attribute.attack_count == 4:
				# 第四发子弹
				# 必定暴击标志
				self.champion.skill.para[1][0] = True
				# 附加物理伤害
				extra_damage = self.champion.skill.para[1][1] * (self.enemy.champion.hp.max_value - self.enemy.champion.hp.value)
				if extra_damage < self.champion.skill.para[1][3]:
					extra_damage = self.champion.skill.para[1][3]
				self.champion.attack_attribute.normal_attack.physical_damage += extra_damage
				# 装弹
				self.champion.skill.para[0][0] = True
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		if self.champion.attack_attribute.attack_count == 4 and self.flag.damage_calculation_flag.normal_attack:
			# 触发爆破专家羁绊效果
			if self.flag.rela_flag['爆破专家'][0]:
				self.champion.relatedness.Blast(self)
	# 攻速转暴击处理
	def As2cr(self,s):
		self.attack_speed_temp *= s
		self.champion.attack_attribute.AD = self.champion.attack_attribute.basic_AD + (self.champion.skill.para[1][2] * \
		(self.attack_speed_temp / self.champion.attack_attribute.attack_speed - 1) * 100)
# 24-50沃利贝尔
class Volibear(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 50
		self.champion.name = 'Volibear'
		self.champion.skill.name = '擂首一击'
		self.champion.skill.describe = ['擂首一击：沃利贝尔开始蓄力，下一','次的普攻将造成额外125(+1.2*额外AD)','的魔法伤害并眩晕敌人2s，若期间受','到硬控，则伤害和眩晕时间翻倍']
		self.champion.hp.max_value = 1000
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 100
		self.champion.attack_attribute.attack_speed = 0.56
		self.champion.attack_attribute.AD = 41
		self.champion.attack_attribute.basic_AD = self.champion.attack_attribute.AD 
		self.champion.defensive_attribute.armor = 38
		self.champion.defensive_attribute.spell_resistance = 35
		self.champion.relatedness.element[0] = '雷霆'
		self.champion.relatedness.profession[0] = '斗士'
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['狂雷渐起',['狂雷渐起：沃利贝尔每次普攻造成伤','害就会获得3%攻速，至多叠加5层，叠','满时，普攻会产生闪电链，对目标一','连线的敌人造成15魔法伤害，持续6s'],False]
		
		self.champion.skill.para = [[125,1.2],2,[False,False,2],[0,5],0.03,[False,Time_count(),6],15]
	
	# 擂首一击属于攻击特效，可以触发卢登，会被闪避，不会被伏击之爪和魔法护盾格挡，闪电链的伤害属于技能伤害
	# 使用技能（施法）
	def Spell_attack(self):
		# 开始蓄力
		self.champion.skill.para[2][0] = True
		# 加快下一次普攻
		self.champion.attack_attribute.normal_attack_time_count = int(0.6 * ((1 / self.champion.attack_attribute.attack_speed * 100) / time_correction[0]))
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal2(self):
		if self.champion.skill.para[2][0]:
			# 判断期间是否收到了控制效果：眩晕、冰冻、压制、缴械、嘲讽
			if self.flag.condition_flag.debuff_dizz_flag or self.flag.condition_flag.debuff_frozen_flag or self.flag.condition_flag.suppress[0] or \
			self.flag.condition_flag.debuff_disarm_flag or self.flag.condition_flag.debuff_taunt_flag:
				self.champion.skill.para[2][1] = True
		# 闪电链持续时间
		if self.champion.skill.para[5][0]:
			if self.champion.skill.para[5][1].Duration(self.champion.skill.para[5][2]):
				# 重置
				self.champion.skill.para[3][0] = 0
				self.champion.attack_attribute.attack_speed /= math.pow((1 + self.champion.skill.para[4]), self.champion.skill.para[3][1])
				self.champion.skill.para[5][0] = False
				self.champion.skill.extra[2][0][2] = False
	# 普攻前特殊效果
	def Special_normal_attack(self):
		# 擂首一击额外魔法伤害
		if self.champion.skill.para[2][0]:
			extra_AD = self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD
			self.champion.attack_attribute.normal_attack.spell_damage += (self.champion.skill.para[0][0] + self.champion.skill.para[0][1] * extra_AD) * self.champion.attack_attribute.spell_power
			if self.champion.skill.para[2][1]:
				self.champion.attack_attribute.normal_attack.spell_damage *= self.champion.skill.para[2][2]
		# 狂雷渐起闪电链
		if self.champion.skill.para[5][0]:
			self.Lightning_chain()
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		if self.flag.damage_calculation_flag.normal_attack:
			# 擂首一击
			if self.champion.skill.para[2][0]:
				# 眩晕
				if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
					if self.champion.skill.para[2][1]:
						dizz_time *= self.champion.skill.para[2][2]
					self.condition.dizz.Add_dizz(self.enemy,dizz_time)
					# 显示
					# self.enemy.flag.special_flag.effect['金色卡牌'][0] = True
				# 触发卢登回声效果
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.normal_attack: 
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 重置
				self.champion.skill.para[2][0] = False
				self.champion.skill.para[2][1] = False
			# 叠加攻速
			if self.champion.skill.para[3][0] < self.champion.skill.para[3][1]:
				self.champion.skill.para[3][0] += 1
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[4])
				if self.champion.skill.para[3][0] == self.champion.skill.para[3][1]:
					self.champion.skill.para[5][0] = True
					self.champion.skill.extra[2][0][2] = True
	# 狂雷渐起闪电链效果
	def Lightning_chain(self):
		# 中心敌人
		if not self.enemy.flag.condition_flag.miss_flag[0]:
			self.Lc_deal(self.enemy)
			# 显示
			self.enemy.flag.special_flag.effect['闪电链'][0] = True
		# 两边敌人(判断是否连线)
		# 中心往上
		for i in range(2):
			if (self.enemy.pos_num - 1 - i >= 0) and (not self.game.LR[~self.position+2][self.enemy.pos_num - 1 - i].flag.condition_flag.death_flag) \
			and (not self.game.LR[~self.position+2][self.enemy.pos_num - 1 - i].flag.condition_flag.miss_flag[0]):
				self.Lc_deal(self.game.LR[~self.position+2][self.enemy.pos_num - 1 - i])
				self.game.LR[~self.position+2][self.enemy.pos_num - 1 - i].flag.special_flag.effect['闪电链'][0] = True
			else:
				break
		# 中心往下
		for i in range(2):
			if (self.enemy.pos_num + 1 + i <= 2) and (not self.game.LR[~self.position+2][self.enemy.pos_num + 1 + i].flag.condition_flag.death_flag) \
			and (not self.game.LR[~self.position+2][self.enemy.pos_num + 1 + i].flag.condition_flag.miss_flag[0]):
				self.Lc_deal(self.game.LR[~self.position+2][self.enemy.pos_num + 1 + i])
				self.game.LR[~self.position+2][self.enemy.pos_num + 1 + i].flag.special_flag.effect['闪电链'][0] = True
			else:
				break
	# 狂雷渐起闪电链伤害计算
	def Lc_deal(self,enemy):
		# 判断敌人的魔法护盾
		if enemy.flag.condition_flag.buff_magic_shield_flag:
			enemy.flag.condition_flag.buff_magic_shield_flag = False
		elif enemy.flag.condition_flag.buff_invincible_flag:
			pass
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[6] * self.champion.attack_attribute.spell_power
			# 伤害计算
			temp_enemy = self.enemy
			self.enemy = enemy
			self.Spell_attack_damage_calculation()
			self.enemy = temp_enemy

# S3 —— 星际战争
# 01-08索拉卡
# 02-15菲兹
# 03-42亚索
# 04-44易
# 05-45慎
# 06-49烬
# 07-51兰博
class Rumble(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 51
		self.champion.name = 'Rumble'
		self.champion.skill.name = '纵火盛宴'
		self.champion.skill.describe = ['纵火盛宴：兰博朝锥形范围内的敌人','施放火焰(持续2.7s且不会被打断)，','每0.3s对目标造成15点魔法伤害并使','目标灼烧，持续3s']
		self.champion.hp.max_value = 880
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 36
		self.champion.defensive_attribute.armor = 28
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '银河机神'
		self.champion.relatedness.profession[0] = '爆破专家'
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [False,[Time_count(),0.3],[0,9],15,3,[False,0,Time_count(),0.1]]

	# 使用技能（施法）
	def Spell_attack(self):
		if not self.champion.skill.para[0]:
			self.champion.skill.para[0] = True
		else:# 重置
			self.champion.skill.para[1][0].value = 0
			self.champion.skill.para[2][0] = 0
			self.champion.skill.para[5][1] = 0
			self.champion.skill.para[5][2].value = 0
		# 火焰特效
		self.champion.skill.para[5][0] = True
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if self.champion.skill.para[0]:
			end_flag = self.champion.skill.para[1][0].Duration(self.champion.skill.para[1][1])
			if end_flag:
				# 计算伤害
				if not self.enemy.flag.condition_flag.death_flag and not self.enemy.flag.condition_flag.miss_flag[0]:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.attack_attribute.spell_power
						# 中心伤害计算
						self.Spell_attack_damage_calculation()
						if self.champion.skill.para[2][0] == 0:
							# 触发卢登回声效果
							if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: 
								self.flag.weapon_flag.ldhs[1] = True
								self.flag.weapon_flag.ldhs[4] = self.enemy
							# 触发爆破专家羁绊效果
							if self.flag.rela_flag['爆破专家'][0]:
								self.champion.relatedness.Blast(self)
						# 灼烧
						if self.flag.damage_calculation_flag.spell_attack:
							self.condition.burn.Add_burn(self.enemy,self.champion.skill.para[4])
							self.enemy.condition.burn.source = self
					# 周围伤害计算
					temp_enemy = self.enemy
					temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
					temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3] * self.champion.attack_attribute.spell_power
					for i in range(2):
						if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
						and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
							self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
							# 处理敌人魔法护盾效果
							if self.enemy.flag.condition_flag.buff_magic_shield_flag:
								self.enemy.condition.magic_shield.Clean(self.enemy.flag)
							else:
								self.Spell_attack_damage_calculation()
							# 触发爆破专家羁绊效果
							if self.flag.rela_flag['爆破专家'][0] and self.champion.skill.para[2][0] == 0:
								self.champion.relatedness.Blast(self)
							# 灼烧
							if self.flag.damage_calculation_flag.spell_attack:
								self.condition.burn.Add_burn(self.enemy,self.champion.skill.para[4])
								self.enemy.condition.burn.source = self
					self.enemy = temp_enemy
					self.champion.skill.aoe[1] = False	
				# DOT计数
				self.champion.skill.para[2][0] += 1
				if self.champion.skill.para[2][0] == self.champion.skill.para[2][1]:
					self.champion.skill.para[2][0] = 0
					self.champion.skill.para[0] = False
					self.flag.special_flag.toxic_smog = False
	# 特殊死亡处理
	def Death_deal_other(self):
		self.champion.skill.para[5][0] = False 
# 08-52吉格斯
class Ziggs(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 52
		self.champion.name = 'Ziggs'
		self.champion.skill.name = '当心炸弹!'
		self.champion.skill.describe = ['当心炸弹!：吉格斯向敌人投掷一颗爆','炸电荷，对目标造成150~300点魔法伤','害，伤害提升幅度基于目标的已损失生','命值']
		self.champion.hp.max_value = 820
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 80
		self.champion.attack_attribute.attack_speed = 0.63
		self.champion.attack_attribute.AD = 38
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 23
		self.champion.relatedness.element[0] = '奥德赛'
		self.champion.relatedness.profession[0] = '爆破专家'
		
		self.champion.skill.para = [150,False]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] + self.champion.skill.para[0] * \
				((self.enemy.champion.hp.max_value - self.enemy.champion.hp.value)/self.enemy.champion.hp.max_value)) * \
				self.champion.attack_attribute.spell_power
			# 伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 触发爆破专家羁绊效果
			if self.flag.rela_flag['爆破专家'][0]:
				self.champion.relatedness.Blast(self)
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 09-53娑娜
class Sona(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 53
		self.champion.name = 'Sona'
		self.champion.skill.name = '坚毅咏叹调'
		self.champion.skill.describe = ['坚毅咏叹调：净化并治疗自己和周围','的队友70点生命值，同时提供70点','护盾，持续4s']
		self.champion.hp.max_value = 830
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 100
		self.champion.attack_attribute.attack_speed = 0.67
		self.champion.attack_attribute.AD = 36
		self.champion.defensive_attribute.armor = 22
		self.champion.defensive_attribute.spell_resistance = 23
		self.champion.relatedness.element[0] = '奥德赛'
		self.champion.relatedness.profession[0] = '秘术师'

		self.champion.skill.para = [70,70,4]

	# 使用技能（施法）
	def Spell_attack(self):
		numTF = [True,self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
		num_pos = [self.pos_num,self.pos_num - 1, self.pos_num +1]
		for i in range(3):
			if numTF[i]:
				if not self.game.LR[self.position][num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[self.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
					# 净化
					self.game.LR[self.position][num_pos[i]].condition.Clean_condition(self.game.LR[self.position][num_pos[i]],2)
					# 治疗
					self.game.LR[self.position][num_pos[i]].champion.hp.HP_restore(self.champion.skill.para[0] * self.champion.attack_attribute.spell_power, self.champion, self.game.LR[self.position][num_pos[i]])
					# 护盾
					self.condition.shield.Add_shield(self.game.LR[self.position][num_pos[i]],self.champion.skill.para[1] * self.champion.attack_attribute.spell_power,self.champion.skill.para[2])
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 10-54阿狸
class Ahri(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 54
		self.champion.name = 'Ahri'
		self.champion.skill.name = '欺诈宝珠'
		self.champion.skill.describe = ['欺诈宝珠：阿狸朝目标发射一颗宝珠，','对其造成120点魔法伤害，随后它会折','返回阿狸处，造成120点真实伤害']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.64
		self.champion.attack_attribute.AD = 34
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '星之守护者'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['摄魂夺魄',['摄魂夺魄：阿狸施放两次技能后，下','一次的技能命中敌人就可以回复25%已','损失生命值'],False]
		self.champion.skill.aoe[0] = True
		self.champion.skill.para = [[120,120],False,[Time_count(),1],[0,False,0.25,False]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 一段伤害
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
			# 伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.damage_calculation_flag.spell_attack:
				# 摄魂夺魄
				if self.champion.skill.para[3][1]:
					# 回复生命值
					value_treatment = int((self.champion.skill.para[3][2] * (self.champion.hp.max_value - self.champion.hp.value)) * self.champion.attack_attribute.spell_power)
					self.champion.hp.HP_restore(value_treatment,self.champion,self)
					self.champion.skill.extra[2][0][2] = False
					self.champion.skill.para[3][3] = True
				if self.flag.weapon_flag.ldhs[0]: # 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0]:
					self.champion.relatedness.Blast(self)
			self.enemy.flag.special_flag.effect['欺诈宝珠'][0] = True
			self.champion.skill.para[1] = True
		# 摄魂夺魄计数
		if not self.champion.skill.para[3][1]:
			self.champion.skill.para[3][0] += 1
			if self.champion.skill.para[3][0] == 2:
				self.champion.skill.extra[2][0][2] = True
				self.champion.skill.para[3][1] = True
		if self.champion.skill.para[3][3]:
			self.champion.skill.para[3][3] = False
			self.champion.skill.para[3][1] = False
			self.champion.skill.para[3][0] = 0
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal2(self):
		# 二段伤害
		if self.champion.skill.para[1] and not self.flag.condition_flag.death_flag:
			end_flag = self.champion.skill.para[2][0].Duration(self.champion.skill.para[2][1])
			if end_flag:
				# 	若目标死亡或不可选取
				if self.enemy.flag.condition_flag.death_flag or self.enemy.flag.condition_flag.miss_flag[0]:
					self.enemy.flag.special_flag.effect['欺诈宝珠'][0] = True
				else:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.real_damage = self.champion.skill.para[0][1] * self.champion.attack_attribute.spell_power
						# 伤害计算
						self.Spell_attack_damage_calculation()
						self.enemy.flag.special_flag.effect['欺诈宝珠'][0] = True
				self.champion.skill.para[1] = False
# 11-55崔斯特
class Twisted(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 55
		self.champion.name = 'Twisted'
		self.skill =[['选牌',['选牌：崔斯特在1.2s内随机选牌，并','在下次普攻时将卡牌丢出，根据卡牌','颜色有三种不同效果——金色：眩晕、','红色：范围伤害、蓝色：范围回蓝']],\
		['金色卡牌',['金色卡牌：对目标造成70点魔法伤害','并眩晕3.5s']],['红色卡牌',['红色卡牌：对目标造成120点魔法伤害，','并对周围敌人造成90点魔法伤害']],\
		['蓝色卡牌',['蓝色卡牌：对目标造成180点魔法伤害，','并回复自己和周围队友30点法力值']]]
		self.champion.skill.name = self.skill[0][0]
		self.champion.skill.describe = self.skill[0][1]
		self.champion.hp.max_value = 880
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 110
		self.champion.attack_attribute.attack_speed = 0.69
		self.champion.attack_attribute.AD = 36
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '未来战士'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['卡牌骗术',['卡牌骗术：每4次攻击，崔斯特的普攻','造成额外50点魔法伤害'],False]
		self.champion.skill.aoe[0] = True
		self.champion.attack_attribute.attack_count = 0                      		# 攻击计数值

		self.champion.skill.para = [False,[Time_count(),0.4,0,3,[0,0]],False,[70,3.5],[120,90],[180,30],50]

		# 卡牌效果属于攻击特效，可以触发卢登和爆破专家羁绊，会被闪避，不会被伏击之爪和魔法护盾格挡，红牌的周围伤害属于技能伤害
	# 使用技能（施法）
	def Spell_attack(self):
		# 开始选牌
		self.champion.skill.para[0] = True
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell = [True,0.5,'选牌']
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal2(self):
		if self.champion.skill.para[0]:
			end_flag = self.champion.skill.para[1][0].Duration(self.champion.skill.para[1][1])
			if end_flag:
				while (self.champion.skill.para[1][4][0] == self.champion.skill.para[1][4][1]):
					self.champion.skill.para[1][4][0] = randint(1,3) 	# 1:金牌；2:红牌；3:蓝牌
				self.champion.skill.para[1][4][1] = self.champion.skill.para[1][4][0]
				# 显示
				self.champion.skill.name = self.skill[self.champion.skill.para[1][4][0]][0]
				self.champion.skill.describe = self.skill[self.champion.skill.para[1][4][0]][1]
				# 计数
				self.champion.skill.para[1][2] += 1
				if self.champion.skill.para[1][2] == self.champion.skill.para[1][3]:
					# 下一次普攻出牌
					self.champion.skill.para[2] = True
					#	加快下一次普攻
					self.champion.attack_attribute.normal_attack_time_count = int(0.4 * ((1 / self.champion.attack_attribute.attack_speed * 100) / time_correction[0]))
					# 重置
					self.champion.skill.para[0] = False
					self.champion.skill.para[1][2] = 0
	# 普攻前特殊效果
	def Special_normal_attack(self):
		# 三色卡牌
		if self.champion.skill.para[2]:
			self.champion.attack_attribute.normal_attack.physical_damage = 0
			# 金色卡牌
			if self.champion.skill.name == '金色卡牌':
				self.champion.attack_attribute.normal_attack.spell_damage = self.champion.skill.para[3][0] * self.champion.attack_attribute.spell_power
			# 红色卡牌
			elif self.champion.skill.name == '红色卡牌':
				self.champion.attack_attribute.normal_attack.spell_damage = self.champion.skill.para[4][0] * self.champion.attack_attribute.spell_power
			# 蓝色卡牌
			elif self.champion.skill.name == '蓝色卡牌':
				self.champion.attack_attribute.normal_attack.spell_damage = self.champion.skill.para[5][0] * self.champion.attack_attribute.spell_power
			# 显示
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
		# 计算额外魔法伤害
		self.champion.attack_attribute.attack_count += 1
		if self.champion.attack_attribute.attack_count == 3:
			pass
		elif self.champion.attack_attribute.attack_count == 4:
			self.champion.attack_attribute.normal_attack.spell_damage += self.champion.skill.para[6] * self.champion.attack_attribute.spell_power
			self.champion.attack_attribute.attack_count = 0
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		# 三色卡牌
		if self.champion.skill.para[2]:
			if self.flag.damage_calculation_flag.normal_attack:
				# 金色卡牌
				if self.champion.skill.name == '金色卡牌':
					# 眩晕
					if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag\
					 and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
						dizz_time = self.champion.skill.para[3][1] / self.enemy.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self.enemy,dizz_time)
						# 显示
						self.enemy.flag.special_flag.effect['金色卡牌'][0] = True
						# 触发爆破炸弹效果
						if self.flag.weapon_flag.bpzd[0] and not self.flag.rela_flag['爆破专家'][0]:
							self.weapon.Bpzd(self,self.enemy)
				# 红色卡牌
				elif self.champion.skill.name == '红色卡牌':
					# 显示
					self.enemy.flag.special_flag.effect['红色卡牌'][0] = True
					# 周围伤害计算
					temp_enemy = self.enemy
					temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
					temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[4][1] * self.champion.attack_attribute.spell_power
					for i in range(2):
						if temp_enemy_numTF[i]:
							if not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
							and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
								self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
								# 处理敌人魔法护盾效果
								if self.enemy.flag.condition_flag.buff_magic_shield_flag:
									self.enemy.condition.magic_shield.Clean(self.enemy.flag)
								else:
									self.Spell_attack_damage_calculation()
								# 显示
								self.enemy.flag.special_flag.effect['红色卡牌'][0] = True
								# 触发爆破专家羁绊效果
								if self.flag.rela_flag['爆破专家'][0]:
									self.champion.relatedness.Blast(self)
					self.enemy = temp_enemy
					self.champion.skill.aoe[1] = False
				# 蓝色卡牌
				elif self.champion.skill.name == '蓝色卡牌':
					# 回蓝
					numTF = [True,self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
					num_pos = [self.pos_num,self.pos_num - 1, self.pos_num +1]
					for i in range(3):
						if numTF[i]:
							if not self.game.LR[self.position][num_pos[i]].flag.condition_flag.death_flag and not \
							self.game.LR[self.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
								self.game.LR[self.position][num_pos[i]].champion.mp.Calculation(self.game.LR[self.position][num_pos[i]],self.champion.skill.para[5][1])
								# 显示
								self.game.LR[self.position][num_pos[i]].flag.special_flag.effect['蓝色卡牌'][0] = True
				# 触发卢登回声效果
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.normal_attack: 
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0]:
					self.champion.relatedness.Blast(self)
			# 重置
			self.champion.skill.name = self.skill[0][0]
			self.champion.skill.describe = self.skill[0][1]
			self.champion.skill.para[2] = False
		if self.flag.weapon_flag.swmd[0] and self.champion.attack_attribute.attack_count == 3 and self.flag.damage_calculation_flag.normal_attack:
			self.condition.injury.Add_injury(self.enemy, self.flag.weapon_flag.swmd[1][0])    				# 触发死亡秘典重伤效果
			self.flag.weapon_flag.swmd[2] = True
# 12-56凯特琳
class Caitlyn(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 56
		self.champion.name = 'Caitlyn'
		self.champion.skill.name = '未来穿甲弹'
		self.champion.skill.describe = ['未来穿甲弹：凯特琳蓄力1.5s后发射','穿甲弹，击破护盾并造成200(+2*额外','AD)物理伤害(每与目标相隔1个单位，','伤害增加100)；凯特琳获得20穿甲']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.74
		self.champion.attack_attribute.AD = 50
		self.champion.attack_attribute.basic_AD = self.champion.attack_attribute.AD
		self.champion.defensive_attribute.armor = 22
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '未来战士'
		self.champion.relatedness.profession[0] = '枪手'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['爆头',['爆头：每次普攻命中敌人时叠加1层充','能(暴击时翻倍)；达到6层后，下一次','普攻爆头，造成(1.0+暴击倍数)倍伤害','爆头次数：0'],False]
		self.champion.attack_attribute.attack_count = 0 
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [20,[Time_count(),1.5],[200,2,100],[0,6,False,1,0,False]]
		self.champion.attack_attribute.armor_penetration += self.champion.skill.para[0]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始蓄力
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[1][0].value = 0
			self.champion.skill.continuous[1] = True
			# 星之守护者羁绊效果
			if self.flag.rela_flag['星之守护者'][0]:
				self.champion.relatedness.Star(self)
			# 魅惑挂坠效果
			if self.flag.weapon_flag.mhgz[0]:
				self.weapon.Mhgz(self)
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[1][1]
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			end_flag = self.champion.skill.para[1][0].Duration(self.champion.skill.para[1][1])
			# 施法结束
			if end_flag:
				# 发射穿甲弹
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					# 破盾
					if not self.enemy.flag.condition_flag.buff_invincible_flag and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
						if self.enemy.condition.shield.value > 0:
							self.enemy.condition.shield.value = 0
							print('凯特琳触发破盾机制！')
					extra_AD = self.champion.attack_attribute.AD - self.champion.attack_attribute.basic_AD
					self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[2][0] + self.champion.skill.para[2][1] \
					* extra_AD + self.champion.skill.para[2][2] * abs(self.pos_num - self.enemy.pos_num)
					# 伤害计算
					self.Spell_attack_damage_calculation()
					# 触发爆破专家羁绊效果
					if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
						self.champion.relatedness.Blast(self)
				self.champion.skill.continuous[1] = False
				self.champion.skill.continuous[2] = True
				# 行为标志处理
				self.flag.move_flag.cast_spell = False
				self.move.current_move = 'normal_attack'
	# 爆头充能计数
	def Headshot(self,n):
		self.champion.skill.para[3][0] += n
		if self.champion.skill.para[3][0] >= self.champion.skill.para[3][1]:
			self.champion.skill.para[3][0] = self.champion.skill.para[3][1]
			self.champion.skill.para[3][2] = True
# 13-57蕾欧娜
class Leona(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 57
		self.champion.name = 'Leona'
		self.champion.skill.name = '赛博屏障'
		self.champion.skill.describe = ['赛博屏障：蕾欧娜开启赛博屏障，在','5s内获得65%减伤，结束时屏障爆裂，','对周围的敌人造成70点魔法伤害并挂','上日光标记(持续5s)']
		self.champion.hp.max_value = 1000
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 110
		self.champion.attack_attribute.attack_speed = 0.55
		self.champion.attack_attribute.AD = 36
		self.champion.defensive_attribute.armor = 40
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '源计划'
		self.champion.relatedness.profession[0] = '护卫'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['日光',['日光：蕾欧娜和她的队友在普攻带有','日光标记的敌人时，额外造成50点魔','法伤害'],False]
		self.champion.skill.aoe[0] = True
		self.champion.skill.para = [[5,0.65,False],70,[False,Time_count(),5]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 减伤效果
		matigation_value = 1 - self.champion.skill.para[0][1]
		self.condition.matigation.Add_matigation(self,matigation_value,self.champion.skill.para[0][0])
		self.champion.skill.para[0][2] = True
		# 显示屏障
		self.flag.special_flag.parclose_flag = True
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal(self):
		if self.champion.skill.para[0][2]:
			# 减伤状态结束
			if not self.flag.condition_flag.buff_matigation_flag:
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
					# 中心伤害计算
					self.Spell_attack_damage_calculation()
					if self.flag.damage_calculation_flag.spell_attack:
						if self.flag.weapon_flag.ldhs[0]: # 触发卢登回声效果
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						# 日光标记
						self.enemy.flag.special_flag.sunlight_sign[0] = True
						self.champion.skill.para[2][0] = True
						# 触发爆破专家羁绊效果
						if self.flag.rela_flag['爆破专家'][0]:
							self.champion.relatedness.Blast(self)
				# 周围伤害计算
				temp_enemy = self.enemy
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
				numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
				num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
				for i in range(2):
					if numTF[i] and (not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.death_flag) \
					and (not self.game.LR[~self.position+2][num_pos[i]].flag.condition_flag.miss_flag[0]):
						self.enemy = self.game.LR[~self.position+2][num_pos[i]]
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						else:
							self.Spell_attack_damage_calculation()
							if self.flag.damage_calculation_flag.spell_attack:
								# 日光标记
								self.enemy.flag.special_flag.sunlight_sign[0] = True
								self.champion.skill.para[2][0] = True
								# 触发爆破专家羁绊效果
								if self.flag.rela_flag['爆破专家'][0]:
									self.champion.relatedness.Blast(self)
					self.enemy = temp_enemy
				self.champion.skill.aoe[1] = False
				# 重置
				self.champion.skill.para[0][2] = False
				self.flag.special_flag.parclose_flag = False
	# 技能特殊效果处理2
	def Special_effect_deal2(self):
		# 清除日光标记
		if self.champion.skill.para[2][0]:
			if self.champion.skill.para[2][1].Duration(self.champion.skill.para[2][2]):
				for i in range(3):
					if self.game.LR[~self.position+2][i].flag.special_flag.sunlight_sign[0] \
					and not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag \
					and not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0]:
						self.game.LR[~self.position+2][i].flag.special_flag.sunlight_sign[0] = False
# 14-58菲奥娜
class Fiora(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 58
		self.champion.name = 'Fiora'
		self.champion.skill.name = '劳伦特心眼刀'
		self.champion.skill.describe = ['劳伦特心眼刀：菲奥娜处于无敌状态，','招架即将到来的攻击，持续1.2s，然','后朝目标方向进行刺击，造成150魔法','伤害和1.5s的眩晕']
		self.champion.hp.max_value = 870
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 0
		self.champion.mp.max_value = 80
		self.champion.attack_attribute.attack_speed = 0.71
		self.champion.attack_attribute.AD = 45
		self.champion.attack_attribute.basic_AD = self.champion.attack_attribute.AD
		self.champion.defensive_attribute.armor = 28
		self.champion.defensive_attribute.spell_resistance = 24
		self.champion.relatedness.element[0] = '源计划'
		self.champion.relatedness.profession[0] = '剑士'

		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),1.2],150,1.5]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始蓄力
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[0][0].value = 0
			# 星之守护者羁绊效果
			if self.flag.rela_flag['星之守护者'][0]:
				self.champion.relatedness.Star(self)
			# 魅惑挂坠效果
			if self.flag.weapon_flag.mhgz[0]:
				self.weapon.Mhgz(self)
			# 进入无敌状态
			self.condition.invincible.Add_invincible(self,self.champion.skill.para[0][1]+0.5)
			self.champion.skill.continuous[1] = True
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[0][1]
			self.Special_spell_attack()
		if self.champion.skill.continuous[1]:
			if self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1]):
				# 退出无敌状态
				self.condition.invincible.Clean(self.flag)
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
					# 伤害计算
					self.Spell_attack_damage_calculation()
					if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
					# 眩晕效果
					if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag\
					 and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
						dizz_time = self.champion.skill.para[2] / self.enemy.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self.enemy,dizz_time)
						# 触发爆破炸弹效果
						if self.flag.weapon_flag.bpzd[0] and not self.flag.rela_flag['爆破专家'][0]:
							self.weapon.Bpzd(self,self.enemy)
					# 触发爆破专家羁绊效果
					if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
						self.champion.relatedness.Blast(self)	

				self.champion.skill.continuous[1] = False
				self.champion.skill.continuous[2] = True
				# 行为标志处理
				self.flag.move_flag.cast_spell = False
				self.move.current_move = 'normal_attack'
# 15-59卡萨丁
class Kassadin(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 59
		self.champion.name = 'Kassadin'
		self.champion.skill.name = '星河脉冲'
		self.champion.skill.describe = ['星河脉冲：卡萨丁闪烁到魔抗最低的','敌人背后，放出一道能量波，对目标','和周围的敌人造成100(+0.5*额外魔抗)','点魔法伤害并缴械3s']
		self.champion.hp.max_value = 870
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 80
		self.champion.mp.max_value = 110
		self.champion.attack_attribute.attack_speed = 0.62
		self.champion.attack_attribute.AD = 39
		self.champion.defensive_attribute.armor = 20
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.defensive_attribute.basic_spell_resistance = self.champion.defensive_attribute.spell_resistance
		self.champion.relatedness.element[0] = '星神'
		self.champion.relatedness.profession[0] = '刺客'
		self.champion.attack_attribute.armor_penetration += 15
		self.champion.attack_attribute.spell_resistance_penetration += 15
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['贤者之石',['贤者之石：卡萨丁所受的魔法伤害减','少20%'],False]

		self.champion.skill.para = [100,0.5,3,0.2]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		sr_min = self.enemy.champion.defensive_attribute.spell_resistance
		enemy_pos_number = 0
		for i in range(3):
			if (not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag) and (not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0]) \
			 and self.game.LR[~self.position+2][i].champion.defensive_attribute.spell_resistance <= sr_min:
				sr_min = self.game.LR[~self.position+2][i].champion.defensive_attribute.spell_resistance
				enemy_pos_number = i
		self.enemy = self.game.LR[~self.position+2][enemy_pos_number]
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			extra_spell_resistance = self.champion.defensive_attribute.spell_resistance - self.champion.defensive_attribute.basic_spell_resistance
			self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] + self.champion.skill.para[1] * extra_spell_resistance) * \
			self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 触发爆破专家羁绊效果
			if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
				self.champion.relatedness.Blast(self)
			# 缴械
			if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag\
			 and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
				disarm_time = self.champion.skill.para[2] / self.enemy.champion.defensive_attribute.tenacity
				self.condition.disarm.Add_disarm(self.enemy,disarm_time)
		# 周围伤害计算
		temp_enemy = self.enemy
		temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
		temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
		for i in range(2):
			if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
			and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
				self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				else:
					extra_spell_resistance = self.champion.defensive_attribute.spell_resistance - self.champion.defensive_attribute.basic_spell_resistance
					self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0] + self.champion.skill.para[1] * extra_spell_resistance) * \
					self.champion.attack_attribute.spell_power
					self.Spell_attack_damage_calculation()
					# 触发爆破专家羁绊效果
					if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
						self.champion.relatedness.Blast(self)
					# 缴械
					if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag\
					 and not (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):
						disarm_time = self.champion.skill.para[2] / self.enemy.champion.defensive_attribute.tenacity
						self.condition.disarm.Add_disarm(self.enemy,disarm_time)
		self.enemy = temp_enemy
		self.champion.skill.aoe[1] = False
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 16-60璐璐
class Lulu(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 60
		self.champion.name = 'Lulu'
		self.champion.skill.name = '帮忙，皮克斯'
		self.champion.skill.describe = ['帮忙，皮克斯：皮克斯在友军身上时，','会为该友军提供180点护盾，持续5s；','皮克斯在敌人身上时，对该敌人造成','180(+额外魔抗)点魔法伤害']
		self.champion.hp.max_value = 820
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 60
		self.champion.attack_attribute.attack_speed = 0.67
		self.champion.attack_attribute.AD = 35
		self.champion.defensive_attribute.armor = 22
		self.champion.defensive_attribute.spell_resistance = 25
		self.basic_spell_resistance = self.champion.defensive_attribute.spell_resistance
		self.champion.relatedness.element[0] = '星神'
		self.champion.relatedness.profession[0] = '秘术师'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['星神伙伴皮克斯',['星神伙伴皮克斯：皮克斯会在友军和','敌人之间周期性移动，在友军身上时，','会协同友军一起普攻，造成15点魔法','伤害'],False]

		self.champion.skill.para = [[180,5],180,15]

	# 使用技能（施法）
	def Spell_attack(self):
		# 皮克斯在友军身上
		if pix.target.position == self.position:
			# 获得护盾
			shield_add = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
			self.condition.shield.Add_shield(pix.target,shield_add,self.champion.skill.para[0][1])
		# 皮克斯在敌人身上
		else:
			temp_enemy = self.enemy
			self.enemy = pix.target
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				extra_spell_resistance = self.champion.defensive_attribute.spell_resistance - self.basic_spell_resistance
				self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[1] + extra_spell_resistance) * self.champion.attack_attribute.spell_power
				# 伤害计算
				self.Spell_attack_damage_calculation()
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
					self.champion.relatedness.Blast(self)
			self.enemy = temp_enemy
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'

	# 特殊死亡处理
	def Death_deal_other(self):
		pix.flag = False
# 17-61卡尔玛
class Karma(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 61
		self.champion.name = 'Karma'
		self.champion.skill.name = '鼓舞'
		self.champion.skill.describe = ['鼓舞：卡尔玛为生命值最低的友军提','供220点护盾，并提升该友军35%的攻','速，持续4s']
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 90
		self.champion.attack_attribute.attack_speed = 0.68
		self.champion.attack_attribute.AD = 39
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '暗星'
		self.champion.relatedness.profession[0] = '秘术师'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['梵咒',['梵咒：卡尔玛施放两次技能后，下一','次的技能作用为对周围队友生效'],False]

		self.champion.skill.para = [[220,0.35],[Time_count() for _ in range(3)],4,[0,False,False]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		hp_min = 5000
		friend_pos_number = 3
		for i in range(3):
			if not self.friend[i].flag.condition_flag.death_flag and not self.friend[i].flag.condition_flag.miss_flag[0] \
			and (self.friend[i].champion.hp.value + self.friend[i].condition.shield.value) <= hp_min and self.friend[i] != self:
				hp_min = self.friend[i].champion.hp.value + self.friend[i].condition.shield.value
				friend_pos_number = i
		if friend_pos_number != 3:
			target = self.friend[friend_pos_number]
		else:
			target = self
		if not self.champion.skill.para[3][1]:
			self.Inspire(target)		
		else: # 梵咒
			numTF = [True,self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
			num_pos = [self.pos_num,self.pos_num - 1, self.pos_num +1]
			for i in range(3):
				if numTF[i]:
					if not self.game.LR[self.position][num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[self.position][num_pos[i]].flag.condition_flag.miss_flag[0]:
						self.Inspire(self.game.LR[self.position][num_pos[i]])
			self.champion.skill.para[3][2] = True
		# 鼓舞计数
		if not self.champion.skill.para[3][1]:
			self.champion.skill.para[3][0] += 1
			if self.champion.skill.para[3][0] == 2:
				self.champion.skill.extra[2][0][2] = True
				self.champion.skill.para[3][1] = True
		if self.champion.skill.para[3][2]:
			self.champion.skill.para[3][2] = False
			self.champion.skill.para[3][1] = False
			self.champion.skill.para[3][0] = 0
			self.champion.skill.extra[2][0][2] = False
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal2(self):
		for i in range(3):
			if self.game.LR[self.position][i].flag.special_flag.effect['鼓舞'][0]:
				if self.champion.skill.para[1][i].Duration(self.champion.skill.para[2]):
					# 恢复攻速
					if self.game.LR[self.position][i].champion.name == 'Jhin':
						self.game.LR[self.position][i].As2cr(1/(math.pow((1 + self.champion.skill.para[0][1]),self.game.LR[self.position][i].flag.special_flag.effect['鼓舞'][1])))
					else:
						self.game.LR[self.position][i].champion.attack_attribute.attack_speed /= math.pow((1 + self.champion.skill.para[0][1]),self.game.LR[self.position][i].flag.special_flag.effect['鼓舞'][1])
					self.game.LR[self.position][i].flag.special_flag.effect['鼓舞'][0] = False
					self.game.LR[self.position][i].flag.special_flag.effect['鼓舞'][1] = 0
	# 提供护盾与攻速
	def Inspire(self,target):
		# 获得护盾
		shield_add = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
		self.condition.shield.Add_shield(target,shield_add,self.champion.skill.para[2])
		if target.flag.special_flag.effect['鼓舞'][1] < 3:
			# 增加攻速
			if target.champion.name == 'Jhin':
				target.As2cr((1 + self.champion.skill.para[0][1]))
			else:
				target.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[0][1])
			target.flag.special_flag.effect['鼓舞'][0] = True
			# 攻速层数
			target.flag.special_flag.effect['鼓舞'][1] += 1
			print('%s鼓舞层数%d' % (target.champion.name,target.flag.special_flag.effect['鼓舞'][1]))
			# 刷新时间
			self.champion.skill.para[1][target.position].value = 0
# 18-62希瓦娜
class Shyvana(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 62
		self.champion.name = 'Shyvana'
		self.skill =[['烈焰吐息',['烈焰吐息：希瓦娜释放离子火球，对','目标造成60点魔法伤害，施加持续','5s的龙血标记，并增加8点怒气']], \
		['烈焰吐息(魔龙形态)',['烈焰吐息(魔龙形态)：烈焰吐息命中','敌人时会爆炸，对目标造成120点魔法','伤害，对周围的敌人造成70点魔法伤','害，施加持续5s的龙血标记并灼烧4s']]]
		self.champion.skill.name = self.skill[0][0]
		self.champion.skill.describe = self.skill[0][1]
		self.champion.hp.max_value = 900
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 100
		self.champion.attack_attribute.attack_speed = 0.59
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 32
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '银河机神'
		self.champion.relatedness.profession[0] = '护卫'
		self.champion.skill.aoe[0] = True
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 2
		self.champion.skill.extra[2][0] = ['银河魔龙降世',['银河魔龙降世：希瓦娜每秒增加4点怒','气，每次普攻增加6点怒气，达到100','时变身银河魔龙，增加300最大生命值','怒气值：0/100'],False]
		self.champion.skill.extra[2][1] = ['龙族血统',['龙族血统：希瓦娜的普攻命中带有龙','血标记的目标时，会造成相当于目标','3%最大生命值的附加魔法伤害'],False]

		self.champion.skill.para = [[60,8],[False,Time_count(),5],[120,70,4],[[Time_count(),4],6,[0,100,0],300,False],0.03]
	# 使用技能（施法）
	def Spell_attack(self):
		if not self.champion.skill.para[3][4]:
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
				# 中心伤害计算
				self.Spell_attack_damage_calculation()
				# 增加怒气
				self.Anger(self.champion.skill.para[0][1])
				if self.flag.damage_calculation_flag.spell_attack:
					# 龙血标记
					self.enemy.flag.special_flag.dragon_sign = True
					self.champion.skill.para[1][0] = True
					if self.flag.weapon_flag.ldhs[0]: # 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
					# 触发爆破专家羁绊效果
					if self.flag.rela_flag['爆破专家'][0]:
						self.champion.relatedness.Blast(self)
		else: # 魔龙形态
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[2][0] * self.champion.attack_attribute.spell_power
				# 中心伤害计算
				self.Spell_attack_damage_calculation()
				if self.flag.damage_calculation_flag.spell_attack:
					if self.flag.weapon_flag.ldhs[0]:											# 触发卢登回声效果
						self.flag.weapon_flag.ldhs[1] = True
						self.flag.weapon_flag.ldhs[4] = self.enemy
					# 龙血标记
					self.enemy.flag.special_flag.dragon_sign = True
					self.champion.skill.para[1][0] = True
					# 触发爆破专家羁绊效果
					if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
						self.champion.relatedness.Blast(self)
					# 灼烧效果(和兰博的灼烧效果会相互覆盖)
					self.condition.burn.Add_burn(self.enemy,self.champion.skill.para[2][2])
					self.enemy.condition.burn.source = self
					# 周围伤害计算(需要中心技能命中才会触发周围伤害)
					temp_enemy = self.enemy
					temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
					temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
					for i in range(2):
						if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
						and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
							self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
							# 处理敌人魔法护盾效果
							if self.enemy.flag.condition_flag.buff_magic_shield_flag:
								self.enemy.condition.magic_shield.Clean(self.enemy.flag)
							else:
								self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[2][1] * self.champion.attack_attribute.spell_power
								self.Spell_attack_damage_calculation()
								# 龙血标记
								self.enemy.flag.special_flag.dragon_sign = True
								# 触发爆破专家羁绊效果
								if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
									self.champion.relatedness.Blast(self)
								# 灼烧效果(和兰博的灼烧效果会相互覆盖)
								self.condition.burn.Add_burn(self.enemy,self.champion.skill.para[2][2])
								self.enemy.condition.burn.source = self
					self.enemy = temp_enemy
					self.champion.skill.aoe[1] = False
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 普攻前特殊效果
	def Special_normal_attack(self):
		if self.enemy.flag.special_flag.dragon_sign:
			self.champion.skill.extra[2][1][2] = True
			# 附加额外魔法伤害
			self.champion.attack_attribute.normal_attack.spell_damage += (self.champion.skill.para[4] * self.enemy.champion.hp.max_value *self.champion.attack_attribute.spell_power)
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		if not self.champion.skill.para[3][4] and self.flag.damage_calculation_flag.normal_attack:
			self.Anger(self.champion.skill.para[3][1])
	# 增加怒气
	def Anger(self,i):
		self.champion.skill.para[3][2][0] += i
		if self.champion.skill.para[3][2][0] >= self.champion.skill.para[3][2][1]:
			self.champion.skill.para[3][2][0] = 100
			# 增加额外生命值(不属于治疗，故不受法强加成)
			self.champion.hp.max_value += self.champion.skill.para[3][3]
			self.champion.hp.value += self.champion.skill.para[3][3]
			self.champion.skill.para[3][4] = True
			self.champion.skill.extra[2][0][2] = True
			self.champion.skill.name = self.skill[1][0]
			self.champion.skill.describe = self.skill[1][1]
		self.champion.skill.para[3][2][2] = int(self.champion.skill.para[3][2][0]/10)
	# 每秒增加怒气
	def Special_effect_deal(self):
		if not self.champion.skill.para[3][4]:
			if self.champion.skill.para[3][0][0].Duration(1):
				self.Anger(self.champion.skill.para[3][0][1])
	# 清除龙血标记
	def Special_effect_deal2(self):
		if self.champion.skill.para[1][0]:
			if self.champion.skill.para[1][1].Duration(self.champion.skill.para[1][2]):
				for i in range(3):
					if self.game.LR[~self.position+2][i].flag.special_flag.dragon_sign and not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag \
					and not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0]:
						self.game.LR[~self.position+2][i].flag.special_flag.dragon_sign = False
# 19-63卢锡安
class Lucian(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 63
		self.champion.name = 'Lucian'
		self.champion.skill.name = '圣枪洗礼'
		self.champion.skill.describe = ['圣枪洗礼：卢锡安在3s内朝敌人发射','10发子弹，每发子弹造成0.3*AD的物','理伤害与40点魔法伤害，并施加攻击','特效']
		self.champion.hp.max_value = 850
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.68
		self.champion.attack_attribute.AD = 42
		self.champion.defensive_attribute.armor = 28
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '源计划'
		self.champion.relatedness.profession[0] = '枪手'
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),0.3,0,10],0.3,40]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始施法
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[0][0].value = 0
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = True
			# 星之守护者羁绊效果
			if self.flag.rela_flag['星之守护者'][0]:
				self.champion.relatedness.Star(self)
			# 魅惑挂坠效果
			if self.flag.weapon_flag.mhgz[0]:
				self.weapon.Mhgz(self)
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[0][1] * self.champion.skill.para[0][3]
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
			# 伤害DOT
			if end_flag:
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					# 属于普攻伤害
					self.champion.attack_attribute.normal_attack.physical_damage = self.champion.skill.para[1] * self.champion.attack_attribute.AD
					self.champion.attack_attribute.normal_attack.spell_damage = self.champion.skill.para[2] * self.champion.attack_attribute.spell_power
					# 伤害计算
					self.Normal_attack_damage_calculation()
					# 计算敌人回蓝
					self.champion.mp.MP_restore_2(self.flag, self, self.enemy, 1)
					if self.flag.damage_calculation_flag.normal_attack and self.champion.skill.para[0][2] == 0:
						if self.flag.weapon_flag.ldhs[0]: # 触发卢登回声效果
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						# 触发爆破专家羁绊效果
						if self.flag.rela_flag['爆破专家'][0]:
							self.champion.relatedness.Blast(self)
				self.champion.skill.para[0][2] += 1
		if self.champion.skill.para[0][2] >= self.champion.skill.para[0][3]:
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = False
			self.champion.skill.continuous[2] = True
			# 行为标志处理
			self.flag.move_flag.cast_spell = False
			self.move.current_move = 'normal_attack'
# 20-64泽拉斯
class Xerath(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 64
		self.champion.name = 'Xerath'
		self.champion.skill.name = '陨灭仪式'
		self.champion.skill.describe = ['陨灭仪式：泽拉斯引导4.5s陨灭仪式，','每过0.9s召唤1颗陨星随机砸向敌人，','造成160点魔法伤害；如果被打断时陨','星数量≤2，则返还50点法力值']
		self.champion.hp.max_value = 830
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 30
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.65
		self.champion.attack_attribute.AD = 30
		self.champion.defensive_attribute.armor = 20
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '暗星'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		# 持续施法技能
		self.champion.skill.continuous[0] = True

		self.champion.skill.para = [[Time_count(),0.9,0,5,False,None],160,[2,50]]

	# 使用技能（施法）
	def Spell_attack(self):
		# 开始施法
		if not self.champion.skill.continuous[1]:
			# 初始化
			self.champion.skill.para[0][0].value = 0
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = True
			self.champion.skill.para[0][4] = True
			self.champion.skill.para[0][5] = self.enemy
			# 星之守护者羁绊效果
			if self.flag.rela_flag['星之守护者'][0]:
				self.champion.relatedness.Star(self)
			# 魅惑挂坠效果
			if self.flag.weapon_flag.mhgz[0]:
				self.weapon.Mhgz(self)
			self.flag.move_flag.show_cast_spell[0] = True
			self.flag.move_flag.show_cast_spell[1] = self.champion.skill.para[0][1] * self.champion.skill.para[0][3]
			self.Special_spell_attack()
		# 施法中
		if self.champion.skill.continuous[1]:
			end_flag = self.champion.skill.para[0][0].Duration(self.champion.skill.para[0][1])
			# 伤害DOT
			if end_flag:
				temp_enemy = self.enemy
				# 选择目标
				self.Target()
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
				else:
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
					# 伤害计算
					self.Spell_attack_damage_calculation()
					self.enemy.flag.special_flag.effect['陨星'][0] = True
					if self.flag.damage_calculation_flag.normal_attack and self.champion.skill.para[0][2] == 0:
						if self.flag.weapon_flag.ldhs[0]: # 触发卢登回声效果
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						# 触发爆破专家羁绊效果
						if self.flag.rela_flag['爆破专家'][0]:
							self.champion.relatedness.Blast(self)
				self.champion.skill.para[0][2] += 1
				self.enemy = temp_enemy
		if self.champion.skill.para[0][2] >= self.champion.skill.para[0][3]:
			self.champion.skill.para[0][2] = 0
			self.champion.skill.continuous[1] = False
			self.champion.skill.continuous[2] = True
			self.champion.skill.para[0][4] = False
			self.enemy = self.champion.skill.para[0][5]
			# 行为标志处理
			self.flag.move_flag.cast_spell = False
			self.move.current_move = 'normal_attack'
	# 判断随机敌人
	def Target(self):
		p = randint(0,2)
		for _ in range(3):
			if not self.game.LR[~self.position+2][p].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][p].flag.condition_flag.miss_flag[0]:
				self.enemy = self.game.LR[~self.position+2][p]
			else:
				p += 1
				if p == 3:
					p = 0
# 21-65艾克
class Ekko(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 65
		self.champion.name = 'Ekko'
		self.champion.skill.name = '时空断裂'
		self.champion.skill.describe = ['时空断裂：艾克冻结时间，然后对每','个敌人造成30(+1.0*AD)点普攻物理伤','害和150点技能魔法伤害(间隔为1s，','第一次攻击若被打断则返还20法力值)']
		self.champion.hp.max_value = 860
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.65
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '源计划'
		self.champion.relatedness.profession[0] = '刺客'
		self.champion.attack_attribute.armor_penetration += 15
		self.champion.attack_attribute.spell_resistance_penetration += 15

		self.champion.skill.para = [[True,Time_count(),1],[30,150],20]
	# 使用技能（施法）
	def Spell_attack(self):
		self.flag.move_flag.show_cast_spell[0] = True
		# 所有人时间静止
		for i in range(2):
			for j in range(3):
				if self.game.LR[i][j] != self and not self.game.LR[i][j].flag.condition_flag.death_flag:
					self.game.LR[i][j].flag.special_flag.motionless_flag = True
		# 先对敌人随机排序
		enemy = [self.game.LR[~self.position+2][0],self.game.LR[~self.position+2][1],self.game.LR[~self.position+2][2]]
		shuffle(enemy)
		# 对所有敌人依次攻击
		for i in range(3):
			# 判断敌人
			if not enemy[i].flag.condition_flag.death_flag and not enemy[i].flag.condition_flag.miss_flag[0]:
				self.enemy = enemy[i]
				# 间隔时间
				self.champion.skill.para[0][0] = True
				while self.champion.skill.para[0][0]:
					if self.champion.skill.para[0][1].Duration(self.champion.skill.para[0][2]):
						self.champion.skill.para[0][0] = False
					# 界面显示刷新
					pos_mouse = pygame.mouse.get_pos()
					self.game.Show_ui(pos_mouse)
					pygame.display.update()
				# 处理敌人魔法护盾效果
				if self.enemy.flag.condition_flag.buff_magic_shield_flag:
					self.enemy.condition.magic_shield.Clean(self.enemy.flag)
				elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
					self.enemy.flag.weapon_flag.fjzz[1] = False
					if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
						dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
						self.condition.dizz.Add_dizz(self,dizz_time)
						# 艾克被打断
						print('艾克被%s的伏击之爪打断施法' % self.enemy.champion.name)
						if i == 0:
							self.champion.mp.Calculation(self,self.champion.skill.para[2])
							print('艾克第一次攻击被打断时，回复%d法力值' % self.champion.skill.para[2])
						break
				# 波比屏障效果
				elif self.enemy.flag.special_flag.obstacle_flag[0]:
					self.enemy.flag.special_flag.obstacle_flag[1].Obstacle(self)
					# 艾克被打断
					print('艾克被波比的屏障打断')
					if i == 0:
						self.champion.mp.Calculation(self,self.champion.skill.para[2])
						print('艾克第一次攻击被打断时，回复%d法力值' % self.champion.skill.para[2])
					break
				else:
					# 普攻伤害初始化
					self.champion.attack_attribute.normal_attack.__init__(self.champion.attack_attribute.AD)
					# 普攻伤害
					self.champion.attack_attribute.normal_attack.physical_damage = self.champion.skill.para[1][0] + self.champion.attack_attribute.AD
					# 计数溢出，则迅速进行下一次普攻
					self.champion.attack_attribute.normal_attack_time_count = 1000
					self.Normal_attack()
					# 计算回蓝
					self.champion.mp.MP_restore_1(self.flag, self, self.enemy)
					# 技能伤害
					self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1][1] * self.champion.attack_attribute.spell_power
					self.Spell_attack_damage_calculation()
					if self.flag.damage_calculation_flag.spell_attack and i == 0:
						if self.flag.weapon_flag.ldhs[0]: # 触发卢登回声效果
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						# 触发爆破专家羁绊效果
						if self.flag.rela_flag['爆破专家'][0]:
							self.champion.relatedness.Blast(self)		
		# 时间静止结束
		for i in range(2):
			for j in range(3):
				if self.game.LR[i][j].flag.special_flag.motionless_flag:
					self.game.LR[i][j].flag.special_flag.motionless_flag = False
		self.flag.move_flag.show_cast_spell[0] = False
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'	
# 22-66伊泽瑞尔
class Ezreal(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 66
		self.champion.name = 'Ezreal'
		self.champion.skill.name = '时间干扰脉冲'
		self.champion.skill.describe = ['时间干扰脉冲：伊泽瑞尔对目标发射','时间干扰脉冲，在命中时爆炸，对目','标造成150魔法伤害，对周围敌人造成','100魔法伤害，并处于破法状态']
		self.champion.hp.max_value = 870
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 140
		self.champion.attack_attribute.attack_speed = 0.68
		self.champion.attack_attribute.AD = 40
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 23
		self.champion.skill.aoe[0] = True
		self.champion.relatedness.element[0] = '未来战士'
		self.champion.relatedness.profession[0] = '爆破专家'

		self.champion.skill.para = [150,100]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.damage_calculation_flag.spell_attack:
				if self.flag.weapon_flag.ldhs[0]:											# 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
					self.champion.relatedness.Blast(self)
				# 破法效果
				if not self.enemy.flag.condition_flag.buff_invincible_flag:
					self.condition.broken.Add_brokrn(self.enemy)
				# 周围伤害计算(需要中心技能命中才会触发周围伤害)
				temp_enemy = self.enemy
				temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
				temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
				for i in range(2):
					if temp_enemy_numTF[i] and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
					and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
						self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						else:
							self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
							self.Spell_attack_damage_calculation()
							# 触发爆破专家羁绊效果
							if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
								self.champion.relatedness.Blast(self)
							# 破法效果
							if not self.enemy.flag.condition_flag.buff_invincible_flag:
								self.condition.broken.Add_brokrn(self.enemy)
				self.enemy = temp_enemy
				self.champion.skill.aoe[1] = False
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
# 23-67奥瑞利安·索尔
class AurelionSol(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 67
		self.champion.name = 'AurelionSol'
		self.champion.skill.name = '舰队出动'
		self.champion.skill.describe = ['舰队出动：奥瑞利安·索尔出动机舱','内的战斗机(上限6台)，战斗机会在','敌人的上空无序徘徊，对途径的敌人','轰炸，每次造成55点魔法伤害']
		self.champion.hp.max_value = 880
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 60
		self.champion.attack_attribute.attack_speed = 0.65
		self.champion.attack_attribute.AD = 35
		self.champion.defensive_attribute.armor = 28
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '奥德赛'
		self.champion.relatedness.profession[0] = '星舰龙神'

		self.champion.skill.para = [[0,6],False,Time_count(),10,55]

	# 使用技能（施法）
	def Spell_attack(self):
		# 按编号出动战斗机
		i = 6
		while i >= 0:
			if not warcraft[self.champion.skill.para[0][0]].flag:
				warcraft[self.champion.skill.para[0][0]].flag = True
				self.champion.skill.para[0][0] += 1
				if self.champion.skill.para[0][0] == self.champion.skill.para[0][1]:
					self.champion.skill.para[0][0] = 0
				break
			else:
				self.champion.skill.para[0][0] += 1
				if self.champion.skill.para[0][0] == self.champion.skill.para[0][1]:
					self.champion.skill.para[0][0] = 0
			i -= 1
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 星舰龙神羁绊效果
	def Special_effect_deal(self):
		if not self.champion.skill.para[1]:
			# 不可阻挡状态
			self.condition.unstoppable.Add_unstoppable(self,100)
			# 缴械状态
			self.condition.disarm.Add_disarm(self,100)
			self.champion.skill.para[1] = True
		# 每秒回蓝
		if self.champion.skill.para[2].Duration(1):
			self.champion.mp.Calculation(self,self.champion.skill.para[3])
	# 特殊死亡处理
	def Death_deal_other(self):
		self.game.warcraft_flag = False
		for num in range(6):
			warcraft[num].flag = False
# 24-68卡兹克
class KhaZix(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 24
		self.champion.name = 'KhaZix'
		self.champion.skill.name = '品尝恐惧'
		self.champion.skill.describe = ['品尝恐惧：卡兹克跃向生命值最低的','敌人，用利爪撕裂敌人，削减目标25%','的护甲并造成100(+1.2*AD)点物理伤','害，若目标孤立无援则造成2倍伤害']
		self.champion.hp.max_value = 840
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 75
		self.champion.attack_attribute.attack_speed = 0.61
		self.champion.attack_attribute.AD = 50
		self.champion.defensive_attribute.armor = 34
		self.champion.defensive_attribute.spell_resistance = 24
		self.champion.relatedness.element[0] = '暗星'
		self.champion.relatedness.profession[0] = '刺客'
		self.champion.attack_attribute.armor_penetration += 15
		self.champion.attack_attribute.spell_resistance_penetration += 15

		self.champion.skill.para = [0.25,100,1.2,2]
	# 使用技能（施法）
	def Spell_attack(self):
		# 判断目标
		# 判断目标
		hp_min = self.enemy.champion.hp.value + self.enemy.condition.shield.value
		enemy_pos_number = 0
		for i in range(3):
			if not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0]\
			 and (self.game.LR[~self.position+2][i].champion.hp.value + self.game.LR[~self.position+2][i].condition.shield.value) <= hp_min:
				hp_min = self.game.LR[~self.position+2][i].champion.hp.value + self.game.LR[~self.position+2][i].condition.shield.value
				enemy_pos_number = i
		self.enemy = self.game.LR[~self.position+2][enemy_pos_number]
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		# 处理伏击之爪
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		# 波比屏障效果
		elif self.enemy.flag.special_flag.obstacle_flag[0]:
			self.enemy.flag.special_flag.obstacle_flag[1].Obstacle(self)
		else:
			# 削甲效果处理
			#	幻影之舞免疫削甲
			if self.enemy.flag.weapon_flag.hyzw[0]:
				self.enemy.flag.weapon_flag.hyzw[1] = True											# 显示触发幻影之舞
			elif self.enemy.flag.condition_flag.buff_invincible_flag or (self.enemy.flag.special_flag.challenge[0] and self != self.enemy.flag.special_flag.challenge[1]):								# 无敌状态免疫削甲
				pass
			else:
				self.enemy.champion.defensive_attribute.armor *= (1 - self.champion.skill.para[0])
				print('%s被卡兹克削甲' % self.enemy.champion.name)
			self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[1] + self.champion.skill.para[2] * self.champion.attack_attribute.AD
			# 孤立无援
			if self.enemy.flag.special_flag.ooal_sign:
				self.champion.attack_attribute.spell_attack.physical_damage *= self.champion.skill.para[3]
			# 伤害计算
			self.Spell_attack_damage_calculation()
			# 触发爆破专家羁绊效果
			if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
				self.champion.relatedness.Blast(self)
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 判断孤立无援
	def Special_effect_deal2(self):
		for i in range(3):
			ooal = [False,False]
			enemy_TF = [i - 1 >= 0, i + 1 <= 2]
			enemy_pos = [i - 1, i + 1]
			if not self.game.LR[~self.position+2][i].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][i].flag.condition_flag.miss_flag[0]:
				for j in range(2):
					if enemy_TF[j]:
						if self.game.LR[~self.position+2][enemy_pos[j]].flag.condition_flag.death_flag or self.game.LR[~self.position+2][enemy_pos[j]].flag.condition_flag.miss_flag[0]:
							ooal[j] = True
					else:
						ooal[j] = True
				if ooal[0] and ooal[1]:
					self.game.LR[~self.position+2][i].flag.special_flag.ooal_sign = True
				else:
					self.game.LR[~self.position+2][i].flag.special_flag.ooal_sign = False
# 25-69金克丝
class Jinx(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 69
		self.champion.name = 'Jinx'
		self.skill = [['砰砰枪——轻机枪',['砰砰枪——轻机枪：普攻会获得8%攻','速加成，可以叠加3次，效果持续到切','换武器为止']],\
		['鱼骨头——火箭发射器',['鱼骨头——火箭发射器：降低8%攻速，','但伤害提升50%，且80%伤害转为魔法','伤害，并会在命中目标时爆炸，对周','围敌人造成60%伤害']]]
		self.champion.skill.name = '枪炮交响曲'
		self.champion.skill.describe = ['枪炮交响曲：金克丝切换她的武器，','每次切换到砰砰枪时会增加20%攻速，','切换到鱼骨头时则增加20%法强，攻速','高于2.5时不再回复法力值']
		self.champion.hp.max_value = 830
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 10
		self.champion.mp.max_value = 70
		self.champion.attack_attribute.attack_speed = 0.74
		self.champion.attack_attribute.AD = 48
		self.champion.defensive_attribute.armor = 25
		self.champion.defensive_attribute.spell_resistance = 22
		self.champion.relatedness.element[0] = '星之守护者'
		self.champion.relatedness.profession[0] = '枪手'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 2
		self.champion.skill.extra[2][0] = [self.skill[0][0],self.skill[0][1],False]
		self.champion.skill.extra[2][1] = ['罪恶快感',['罪恶快感：金克丝击杀敌人时获得额','外30%攻速，持续6s'],False]
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [0,[0.2,0,0.2,0,False],[True,0.08,0,3],[False,0.08,0.5,0.8,0.6],[False,0.3,Time_count(),6],2.5]
	# 使用技能（施法）
	def Spell_attack(self):
		# 切枪
		self.champion.skill.para[0] = ~self.champion.skill.para[0]+2
		self.champion.skill.extra[2][0] = [self.skill[self.champion.skill.para[0]][0],self.skill[self.champion.skill.para[0]][1],False]
		# 切枪标志
		self.champion.skill.para[1][4] = True
		# 切换为砰砰枪
		if self.champion.skill.para[0] == 0:
			# 重置鱼骨头
			self.champion.skill.para[3][0] = False
			self.champion.attack_attribute.attack_speed /= (1 - self.champion.skill.para[3][1])
			# 提升攻速
			self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[1][0])
			self.champion.skill.para[1][1] += 1
			print('切换为砰砰枪加攻速，层数：%d' % self.champion.skill.para[1][1])
			self.champion.skill.para[2][0] = True
		# 切换为鱼骨头
		if self.champion.skill.para[0] == 1:
			# 重置砰砰枪
			self.champion.skill.para[2][0] = False
			self.champion.attack_attribute.attack_speed /= (math.pow((1 + self.champion.skill.para[2][1]),self.champion.skill.para[2][2]))
			self.champion.skill.para[2][2] = 0
			# 提升法强
			self.champion.attack_attribute.spell_power += self.champion.skill.para[1][2]
			self.champion.skill.para[1][3] += 1
			print('切换为鱼骨头加法强，层数：%d' % self.champion.skill.para[1][3])
			# 降攻速
			self.champion.attack_attribute.attack_speed *= (1 - self.champion.skill.para[3][1])
			self.champion.skill.para[3][0] = True
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 普攻前特殊效果
	def Special_normal_attack(self):
		# 鱼骨头：物理伤害提升20%，再部分转为魔法伤害
		if self.champion.skill.para[3][0]:
			self.champion.attack_attribute.normal_attack.physical_damage *= (1 + self.champion.skill.para[3][2])
			self.champion.attack_attribute.normal_attack.spell_damage += (self.champion.attack_attribute.normal_attack.physical_damage * self.champion.skill.para[3][3] \
			 * self.champion.attack_attribute.spell_power)
			self.champion.attack_attribute.normal_attack.physical_damage *= (1 - self.champion.skill.para[3][3])
	# 普攻后特殊效果
	def Special_normal_attack2(self):
		if self.flag.damage_calculation_flag.normal_attack:
			# 金克丝转爆破专家时，切枪后的第一下普攻触发爆破专家羁绊效果
			if self.champion.skill.para[1][4] and self.flag.rela_flag['爆破专家'][0]:
				self.champion.relatedness.Blast(self)
			# 砰砰枪普攻命中后叠加攻速
			if self.champion.skill.para[2][0]:
				if self.champion.skill.para[2][2] < self.champion.skill.para[2][3]:
					self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[2][1])
					self.champion.skill.para[2][2] += 1
			# 鱼骨头普攻命中后爆炸产生对周围敌人造成伤害(属于技能伤害)，不会被抵挡，不触发卢登，切枪后的第一下普攻可以触发爆破专家羁绊
			if self.champion.skill.para[3][0]:
				# 显示效果
				self.enemy.flag.special_flag.effect['鱼骨头'][0] = True
				# 判断目标
				temp_enemy = self.enemy
				temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
				temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
				for i in range(2):
					if temp_enemy_numTF[i]:
						if not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
						and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
							self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
							# 计算伤害
							self.champion.attack_attribute.spell_attack.physical_damage = self.champion.skill.para[3][4] * self.champion.attack_attribute.AD * \
							(1 + self.champion.skill.para[3][2]) * (1 - self.champion.skill.para[3][3])
							self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[3][4] * self.champion.attack_attribute.AD * \
							(1 + self.champion.skill.para[3][2]) * self.champion.skill.para[3][3] * self.champion.attack_attribute.spell_power
							self.Spell_attack_damage_calculation()
							# 触发爆破专家羁绊效果
							if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack and self.champion.skill.para[1][4]:
								self.champion.relatedness.Blast(self)
							# 显示效果
							self.enemy.flag.special_flag.effect['鱼骨头'][0] = True
				self.enemy = temp_enemy
				self.champion.skill.aoe[1] = False
		if self.champion.skill.para[1][4]:
			self.champion.skill.para[1][4] = False
	# 罪恶快感持续时间
	def Special_effect_deal(self):
		if self.champion.skill.para[4][0]:
			if self.champion.skill.para[4][2].Duration(self.champion.skill.para[4][3]):
				self.champion.attack_attribute.attack_speed /= (1 + self.champion.skill.para[4][1])
				self.champion.skill.para[4][0] = False
	# 罪恶快感
	def Kill_deal(self):
		if self.flag.special_flag.kill[0]:
			if not self.champion.skill.para[4][0]:
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[4][1])
				self.champion.skill.para[4][0] = True
				self.champion.skill.extra[2][1][2] = True
			else:
				self.champion.skill.para[4][2].value = 0
# 26-70安妮
class Annie(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 70
		self.champion.name = 'Annie'
		self.skill = [['提伯斯之怒',['提伯斯之怒：安妮召唤提伯斯，并对','周围敌人造成100点魔法伤害，提伯斯','的普攻会造成50点魔法伤害且提伯斯','会承担安妮受到的70%的伤害']],\
		['银河护盾',['银河护盾：安妮召唤提伯斯之后技能','改为银河护盾，为自己和提伯斯提供','80点护盾并提升10%的攻速，持续4s']]]
		self.champion.skill.name = self.skill[0][0]
		self.champion.skill.describe = self.skill[0][1]
		self.champion.hp.max_value = 500
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 10
		self.champion.mp.max_value = 100
		self.champion.attack_attribute.attack_speed = 0.67
		self.champion.attack_attribute.AD = 37
		self.champion.defensive_attribute.armor = 20
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '银河机神'
		self.champion.relatedness.profession[0] = '法师'
		self.champion.mp.basic_MP_restore = 20 # 法师的基础回蓝翻2倍
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [100,50,0.7,80,4,0.10,[0,0],[False,Time_count()]]
	# 使用技能（施法）
	def Spell_attack(self):
		if self.champion.skill.name == '提伯斯之怒':
			# 召唤提伯斯
			tibbers.flag = True
			tibbers.Annie = self
			tibbers.position = self.position
			tibbers.pos_num = self.pos_num
			tibbers.enemy = self.enemy
			# 召唤时的AOE伤害
			# 处理敌人魔法护盾效果
			if self.enemy.flag.condition_flag.buff_magic_shield_flag:
				self.enemy.condition.magic_shield.Clean(self.enemy.flag)
			elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
				self.enemy.flag.weapon_flag.fjzz[1] = False
				if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
					dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
					self.condition.dizz.Add_dizz(self,dizz_time)
			else:
				self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
				# 中心伤害计算
				self.Spell_attack_damage_calculation()
				if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
					self.champion.relatedness.Blast(self)
			# 周围伤害计算
			temp_enemy = self.enemy
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
			temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
			for i in range(2):
				if temp_enemy_numTF[i]:
					if not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
						self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
						# 处理敌人魔法护盾效果
						if self.enemy.flag.condition_flag.buff_magic_shield_flag:
							self.enemy.condition.magic_shield.Clean(self.enemy.flag)
						else:
							self.Spell_attack_damage_calculation()
							# 触发爆破专家羁绊效果
							if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
								self.champion.relatedness.Blast(self)
			self.enemy = temp_enemy
			self.champion.skill.aoe[1] = False
			self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
			# 切换技能
			self.champion.skill.name = self.skill[1][0]
			self.champion.skill.describe = self.skill[1][1]
		else:
			# 安妮获得护盾
			shield_add = self.champion.skill.para[3] * self.champion.attack_attribute.spell_power
			self.condition.shield.Add_shield(self,shield_add,self.champion.skill.para[4])
			if self.champion.skill.para[6][0] < 3:
				# 攻速提升
				self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[5])
				self.champion.skill.para[6][0] += 1
			# 提伯斯获得护盾
			if tibbers.flag:
				tibbers.shield_value += shield_add
				tibbers.shield_time = Max(self.champion.skill.para[4],int((tibbers.shield_time*100 - tibbers.shield_time_count.value)/100))
				tibbers.shield_time_count.value = 0
				tibbers.shield_flag = True
				if self.champion.skill.para[6][1] < 3:
					# 攻速提升
					tibbers.attack_speed *= (1 + self.champion.skill.para[5])
					self.champion.skill.para[6][1] += 1
			self.champion.skill.para[7][0] = True
			self.champion.skill.para[7][1].value = 0
			self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 技能特殊效果处理
	def Special_effect_deal2(self):
		if self.champion.skill.para[7][0]:
			if self.champion.skill.para[7][1].Duration(self.champion.skill.para[4]):
				self.champion.skill.para[7][0] = False
				# 恢复攻速
				self.champion.attack_attribute.attack_speed /= math.pow((1 + self.champion.skill.para[5]),self.champion.skill.para[6][0])
				self.champion.skill.para[6][0] = 0
				if tibbers.flag:
					tibbers.attack_speed /= math.pow((1 + self.champion.skill.para[5]),self.champion.skill.para[6][1])
					self.champion.skill.para[6][1] = 0
	# 特殊死亡处理
	def Death_deal_other(self):
		# 安妮死亡时提伯斯消失
		tibbers.flag = False
# 27-71波比
class Poppy(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 71
		self.champion.name = 'Poppy'
		self.champion.skill.name = '盾牌投掷'
		self.champion.skill.describe = ['盾牌投掷：波比向随机一个敌人投掷','盾牌，造成100点魔法伤害，圆盾随后','会折返至波比处，为她提供230点护盾，','持续5s']
		self.champion.hp.max_value = 980
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 110
		self.champion.attack_attribute.attack_speed = 0.57
		self.champion.attack_attribute.AD = 38
		self.champion.defensive_attribute.armor = 35
		self.champion.defensive_attribute.spell_resistance = 25
		self.champion.relatedness.element[0] = '星之守护者'
		self.champion.relatedness.profession[0] = '护卫'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['坚定风采',['坚定风采：波比施放技能后会在周围','架起屏障(持续3s)，阻挡刺客的突进','(不包括卡萨丁的闪烁)，阻挡成功时','对目标造成100点魔法伤害并眩晕1s'],False]
		
		self.champion.skill.para = [[100,230,5],[False,None],[Time_count(),0.5],[False,Time_count()],[False,Time_count(),3],[100,1]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 随机目标
		p = randint(0,2)
		for i in range(3):
			if not self.game.LR[~self.position+2][p].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][p].flag.condition_flag.miss_flag[0]:
				self.champion.skill.para[1][1] = self.game.LR[~self.position+2][p]
				break
			else:
				p += 1
				if p == 3:
					p = 0
		# 投掷盾牌
		self.champion.skill.para[1][0] = True
		# 坚定风采
		self.champion.skill.para[4][0] = True
		self.game.obstacle_flag = [True,self]
		self.flag.special_flag.obstacle_flag = [True,self]
		self.champion.skill.extra[2][0][2] = True
		numTF = [self.pos_num - 1 >= 0, self.pos_num + 1 <= 2]
		num_pos = [self.pos_num - 1, self.pos_num + 1]
		for i in range(2):
			if numTF[i]:
				self.game.LR[self.position][num_pos[i]].flag.special_flag.obstacle_flag = [True,self]
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 盾牌投掷
	def Special_effect_deal2(self):
		# 圆盾
		if self.champion.skill.para[1][0]:
			end_flag = self.champion.skill.para[2][0].Duration(self.champion.skill.para[2][1])
			if end_flag:
				temp_enemy = self.enemy
				self.enemy = self.champion.skill.para[1][1]
				# 	若目标死亡或不可选取、不会折返
				if self.enemy.flag.condition_flag.death_flag or self.enemy.flag.condition_flag.miss_flag[0]:
					self.enemy.flag.special_flag.effect['圆盾'][0] = True
				else:
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
						self.enemy.flag.weapon_flag.fjzz[1] = False
						if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
							dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
							self.condition.dizz.Add_dizz(self,dizz_time)
					else:
						self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
						# 伤害计算
						self.Spell_attack_damage_calculation()
						if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
							self.flag.weapon_flag.ldhs[1] = True
							self.flag.weapon_flag.ldhs[4] = self.enemy
						# 触发爆破专家羁绊效果
						if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
							self.champion.relatedness.Blast(self)
						self.enemy.flag.special_flag.effect['圆盾'][0] = True
						self.champion.skill.para[1][0] = False
						self.champion.skill.para[3][0] = True
				self.enemy = temp_enemy
	# 盾牌折返/坚定风采持续时间
	def Special_effect_deal(self):
		if self.champion.skill.para[3][0]:
			end_flag = self.champion.skill.para[3][1].Duration(self.champion.skill.para[2][1])
			if end_flag:
				shield_add = self.champion.skill.para[0][1] * self.champion.attack_attribute.spell_power
				self.condition.shield.Add_shield(self,shield_add,self.champion.skill.para[0][2])
				self.flag.special_flag.effect['圆盾'][0] = True
				self.champion.skill.para[3][0] = False
		# 坚定风采持续时间
		if self.champion.skill.para[4][0]:
			if self.champion.skill.para[4][1].Duration(self.champion.skill.para[4][2]):
				self.champion.skill.extra[2][0][2] = False
				self.champion.skill.para[4][0] = False
				self.game.obstacle_flag[0] = False
				for i in range(3):
					self.friend[i].flag.special_flag.obstacle_flag[0] = False
	# 坚定风采
	def Obstacle(self,enemy):
		temp_enemy = self.enemy
		self.enemy = enemy
		self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[5][0] * self.champion.attack_attribute.spell_power
		# 伤害计算
		self.Spell_attack_damage_calculation()
		# 眩晕效果
		if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
			dizz_time = self.champion.skill.para[5][1] / self.enemy.champion.defensive_attribute.tenacity
			self.condition.dizz.Add_dizz(self.enemy,dizz_time)
			# 触发爆破炸弹效果
			if self.flag.weapon_flag.bpzd[0] and not self.flag.rela_flag['爆破专家'][0]:
				self.weapon.Bpzd(self,self.enemy)
		print('%s被波比的屏障所阻挡' % enemy.champion.name)
		self.enemy = temp_enemy
	# 特殊死亡处理
	def Death_deal_other(self):
		self.champion.skill.extra[2][0][2] = False
		self.champion.skill.para[4][0] = False
		self.game.obstacle_flag[0] = False
		for i in range(3):
			self.friend[i].flag.special_flag.obstacle_flag[0] = False
# 28-72赵信
class ZhaoXin(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 72
		self.champion.name = 'ZhaoXin'
		self.champion.skill.name = '新月护卫'
		self.champion.skill.describe = ['新月护卫：赵信向目标发起挑战，猛','烈挥舞长枪，对目标造成40魔法伤害，','对周围敌人造成80(+15%目标当前生','命值)魔法伤害并晕眩2s']
		self.champion.hp.max_value = 890
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 40
		self.champion.mp.max_value = 130
		self.champion.attack_attribute.attack_speed = 0.68
		self.champion.attack_attribute.AD = 39
		self.champion.defensive_attribute.armor = 38
		self.champion.defensive_attribute.spell_resistance = 20
		self.champion.relatedness.element[0] = '星神'
		self.champion.relatedness.profession[0] = '护卫'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['挑战',['挑战：赵信成功施放新月护卫后5s内','进入挑战状态，获得额外40%攻速，并','且不受挑战目标以外敌人的伤害'],False]
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [[40,80,0.15],2,[5,0.4,False,Time_count()]]
	# 使用技能（施法）
	def Spell_attack(self):
		# 记录目标的当前生命值
		temp_hp = self.enemy.champion.hp.value
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0][0] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.damage_calculation_flag.spell_attack:
				if self.flag.weapon_flag.ldhs[0]:											# 触发卢登回声效果
					self.flag.weapon_flag.ldhs[1] = True
					self.flag.weapon_flag.ldhs[4] = self.enemy
				# 触发爆破专家羁绊效果
				if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
					self.champion.relatedness.Blast(self)
			# 发起挑战
			self.flag.special_flag.challenge = [True,self.enemy,False]
			self.champion.skill.para[2][2] = True
			self.enemy.flag.special_flag.challenge[2] = True
			self.enemy.enemy = self
			# 加攻速
			self.champion.attack_attribute.attack_speed *= (1 + self.champion.skill.para[2][1])
			self.champion.skill.extra[2][0][2] = True
		# 周围伤害计算
		temp_enemy = self.enemy
		self.champion.attack_attribute.spell_attack.spell_damage = (self.champion.skill.para[0][1] + self.champion.skill.para[0][2] * temp_hp) * self.champion.attack_attribute.spell_power
		temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
		temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
		for i in range(2):
			if temp_enemy_numTF[i]:
				if not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag \
				and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					else:
						self.Spell_attack_damage_calculation()
						if not self.enemy.flag.condition_flag.buff_invincible_flag and not self.enemy.flag.condition_flag.buff_unstoppable_flag:
							# 眩晕效果处理
							dizz_time = self.champion.skill.para[1] / self.enemy.champion.defensive_attribute.tenacity
							self.enemy.condition.dizz.Add_dizz(self.enemy,dizz_time)
							# 触发爆破炸弹效果
							if self.flag.weapon_flag.bpzd[0] and not self.flag.rela_flag['爆破专家'][0]:
								self.weapon.Bpzd(self,self.enemy)
						# 触发爆破专家羁绊效果
						if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
							self.champion.relatedness.Blast(self)
		self.enemy = temp_enemy
		self.champion.skill.aoe[1] = False
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 挑战期间
	def Special_effect_deal(self):
		if self.champion.skill.para[2][2]:
			# 挑战目标死亡或不可选取时退出挑战
			if self.flag.special_flag.challenge[1].flag.condition_flag.death_flag or self.flag.special_flag.challenge[1].flag.condition_flag.miss_flag[0] \
			or self.champion.skill.para[2][3].Duration(self.champion.skill.para[2][0]):
				# 恢复攻速
				self.champion.attack_attribute.attack_speed /= (1 + self.champion.skill.para[2][1])
				# 退出挑战
				self.champion.skill.para[2][2] = False
				if not self.flag.special_flag.challenge[1].flag.condition_flag.death_flag and not self.flag.special_flag.challenge[1].flag.condition_flag.miss_flag[0]:
					self.flag.special_flag.challenge[1].flag.special_flag.challenge[2] = False
				self.flag.special_flag.challenge = [False,None,False]
				self.champion.skill.extra[2][0][2] = False
	# 特殊死亡处理
	def Death_deal_other(self):
		if self.champion.skill.para[2][2]:
			self.flag.special_flag.challenge[1].flag.special_flag.challenge[2] = False
# 29-73黑默丁格
class Heimerdinger(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 73
		self.champion.name = 'Heimerdinger'
		self.skill = [['H-28G进化炮台',['H-28G进化炮台：放置持续9s的炮台(上','限3个)，每次攻击造成25点魔法伤害，','且每第3下攻击会对黑默丁格当前目标','进行镭射攻击，造成50点魔法伤害']],\
		['H-28Q尖端炮台',['H-28Q尖端炮台：放置升级后的超级炮','台，持续时间增长为12s且攻速更快，','普通攻击造成40点魔法伤害，镭射攻','击造成80点魔法伤害']]]
		self.champion.skill.name = self.skill[0][0]
		self.champion.skill.describe = self.skill[0][1]
		self.champion.hp.max_value = 550
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 20
		self.champion.mp.max_value = 45
		self.champion.attack_attribute.attack_speed = 0.7
		self.champion.attack_attribute.AD = 36
		self.champion.defensive_attribute.armor = 18
		self.champion.defensive_attribute.spell_resistance = 18
		self.spell_power_temp = self.champion.attack_attribute.spell_power
		self.champion.relatedness.element[0] = '异星人'
		self.champion.relatedness.profession[0] = '爆破专家'
		self.champion.skill.extra[0] = True
		self.champion.skill.extra[1] = 1
		self.champion.skill.extra[2][0] = ['升级!!!',['升级!!!：黑默丁格放置两个炮台后，','下一个炮台升级为H-28Q尖端炮台'],False]

		self.champion.skill.para = [[9,25,50],[12,40,80],[0,2,False],[0.1,0.1,0.9]]
	
	# 使用技能（施法）
	def Spell_attack(self):
		# 召唤炮台
		pos_num = self.enemy.pos_num
		for i in range(3):
			if not battery[pos_num].flag:
				battery[pos_num].flag = True
				battery[pos_num].position = self.position
				battery[pos_num].Heimerdinger = self
				self.flag.move_flag.show_cast_spell[2] = self.champion.skill.name
				# 判断是否为超级炮台
				if self.champion.skill.para[2][2]:
					battery[pos_num].super_flag = True
					battery[pos_num].para = self.champion.skill.para[1]
					battery[pos_num].attack_speed = 0.74
					battery[pos_num].Init()
					self.champion.skill.para[2][2] = False
					self.champion.skill.para[2][0] = 0
					self.champion.skill.name = self.skill[0][0]
					self.champion.skill.describe = self.skill[0][1]
				else:
					battery[pos_num].super_flag = False
					battery[pos_num].para = self.champion.skill.para[0]
					battery[pos_num].attack_speed = 0.7
					battery[pos_num].Init()
					self.champion.skill.para[2][0] += 1
					if self.champion.skill.para[2][0] == self.champion.skill.para[2][1]:
						self.champion.skill.extra[2][0][2] = True
						self.champion.skill.para[2][2] = True
						self.champion.skill.name = self.skill[1][0]
						self.champion.skill.describe = self.skill[1][1]
				break
			else:
				pos_num += 1
				if pos_num == 3:
					pos_num = 0
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 异星人羁绊效果
	def Special_effect_deal(self):
		# 判断友方单位数量
		num = 0
		#	英雄(不包括自己)、炮台
		for i in range(3):
			if self.game.LR[self.position][i] != self and not self.game.LR[self.position][i].flag.condition_flag.death_flag:
				num += 1
			if battery[i].flag:
				num += 1
		#	皮克斯、提伯斯、已出舱的战斗机
		if pix.flag and pix.Lulu.position == self.position:
			num += 1
		if tibbers.flag and tibbers.Annie.position == self.position:
			num += 1
		for i in range(6):
			if warcraft[i].flag and warcraft[i].AurelionSol.position == self.position:
				num += 1
		# 加法强
		self.champion.attack_attribute.spell_power = self.spell_power_temp + self.champion.skill.para[3][0] * num
		# 加减伤
		matigation_value = 1 - (self.champion.skill.para[3][1] * num)
		if matigation_value < (1 - self.champion.skill.para[3][2]):
			matigation_value = 1 - self.champion.skill.para[3][2]
		self.condition.matigation.Add_matigation(self,matigation_value,0.5)
	# 特殊死亡处理
	def Death_deal_other(self):
		# 死亡时炮台消失
		for i in range(3):
			battery[i].flag = False
	# 加法强
	def Add_spell_power(self,sp):
		self.spell_power_temp += sp
		self.champion.attack_attribute.spell_power += sp

# 机神盖伦
class Garen(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 74
		self.champion.name = 'Garen'
		self.champion.skill.name = '机神裁决'
		self.champion.skill.describe = ['机神裁决：银河魔装机神盖伦召唤一','道毁灭冲击，对目标造成180点魔法伤','害，对周围敌人造成120点魔法伤害']
		self.champion.hp.max_value = 1000
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.mp.value = 50
		self.champion.mp.max_value = 120
		self.champion.attack_attribute.attack_speed = 0.71
		self.champion.attack_attribute.AD = 46
		self.champion.defensive_attribute.armor = 35
		self.champion.defensive_attribute.spell_resistance = 30
		self.champion.relatedness.element[0] = '银河魔装机神'
		self.champion.relatedness.profession[0] = '先锋'
		self.champion.skill.aoe[0] = True

		self.champion.skill.para = [180,120]
	# 使用技能（施法）
	def Spell_attack(self):
		# 处理敌人魔法护盾效果
		if self.enemy.flag.condition_flag.buff_magic_shield_flag:
			self.enemy.condition.magic_shield.Clean(self.enemy.flag)
		elif self.enemy.flag.weapon_flag.fjzz[0] and self.enemy.flag.weapon_flag.fjzz[1]: 	# 触发敌人伏击之爪效果
			self.enemy.flag.weapon_flag.fjzz[1] = False
			if not self.flag.condition_flag.buff_invincible_flag and not self.flag.condition_flag.buff_unstoppable_flag:
				dizz_time = self.enemy.flag.weapon_flag.fjzz[2] / self.champion.defensive_attribute.tenacity
				self.condition.dizz.Add_dizz(self,dizz_time)
		else:
			self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[0] * self.champion.attack_attribute.spell_power
			# 中心伤害计算
			self.Spell_attack_damage_calculation()
			if self.flag.weapon_flag.ldhs[0] and self.flag.damage_calculation_flag.spell_attack: # 触发卢登回声效果
				self.flag.weapon_flag.ldhs[1] = True
				self.flag.weapon_flag.ldhs[4] = self.enemy
			# 触发爆破专家羁绊效果
			if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
				self.champion.relatedness.Blast(self)
		# 周围伤害计算
		temp_enemy = self.enemy
		self.champion.attack_attribute.spell_attack.spell_damage = self.champion.skill.para[1] * self.champion.attack_attribute.spell_power
		temp_enemy_numTF = [temp_enemy.pos_num - 1 >= 0, temp_enemy.pos_num + 1 <= 2]
		temp_enemy_num_pos = [temp_enemy.pos_num - 1, temp_enemy.pos_num + 1]
		for i in range(2):
			if temp_enemy_numTF[i]:
				if not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.death_flag and not self.game.LR[~self.position+2][temp_enemy_num_pos[i]].flag.condition_flag.miss_flag[0]:
					self.enemy = self.game.LR[~self.position+2][temp_enemy_num_pos[i]]
					# 处理敌人魔法护盾效果
					if self.enemy.flag.condition_flag.buff_magic_shield_flag:
						self.enemy.condition.magic_shield.Clean(self.enemy.flag)
					else:
						self.Spell_attack_damage_calculation()
						# 触发爆破专家羁绊效果
						if self.flag.rela_flag['爆破专家'][0] and self.flag.damage_calculation_flag.spell_attack:
							self.champion.relatedness.Blast(self)
		self.enemy = temp_enemy
		self.champion.skill.aoe[1] = False
		# 星之守护者羁绊效果
		if self.flag.rela_flag['星之守护者'][0]:
			self.champion.relatedness.Star(self)
		# 魅惑挂坠效果
		if self.flag.weapon_flag.mhgz[0]:
			self.weapon.Mhgz(self)
		# 行为标志处理
		self.flag.move_flag.show_cast_spell[0] = True
		self.flag.move_flag.cast_spell = False
		self.Special_spell_attack()
		self.move.current_move = 'normal_attack'
	# 机甲解体
	def Death_deal_other(self):
		self.game.LR[self.position][self.pos_num] = self.game.MechWarrior_flag[self.position][4]
		self.game.LR_ui[self.position][self.pos_num] = Champion_Interface(self.game.screen,self.game.MechWarrior_flag[self.position][4],self.game)
		for j in range(3):
			if j != self.pos_num:
				self.game.LR[self.position][j].friend[self.pos_num] = self.game.LR[self.position][self.pos_num]
		for i in range(3):
			if self.game.LR[self.position][i].flag.rela_flag['银河机神'][3][0]:
				# 不可选取计数溢出，退出不可选取状态
				self.game.LR[self.position][i].condition.miss.time = 0
				self.game.LR[self.position][i].flag.rela_flag['银河机神'][3][0] = False
NormalGaren = [Garen() for _ in range(2)]
SuperGaren = Garen()

# 虚空兽
class VoidMonster(Champion):
	def __init__(self):
		super().__init__()
		self.champion.number = 303
		self.champion.name = 'VoidMonster'
		self.champion.skill.name = '虚空入侵'
		self.champion.skill.describe = ['虚空入侵：虚空兽获得额外AD，数值','等于召唤它的英雄的护甲与魔抗值和','×25%']
		self.champion.hp.max_value = 700
		self.champion.hp.value = self.champion.hp.max_value
		self.champion.skill.active_skill = False
		self.champion.mp.value = 0
		self.champion.mp.max_value = 0
		self.champion.attack_attribute.attack_speed = 0.65
		self.champion.attack_attribute.AD = 40
		self.champion.attack_attribute.crit_mechanism.crit = 0
		self.champion.attack_attribute.crit_mechanism.crit_multiple = 0
		self.champion.defensive_attribute.armor = 35
		self.champion.defensive_attribute.spell_resistance = 30
		self.champion.defensive_attribute.dodge_mechanism.dodge = 0
		self.champion.relatedness.element[0] = '虚空'
		self.champion.relatedness.profession[0] = '先锋'

		self.champion.skill.para = [0.25,False]
	# 使用技能（施法）
	def Spell_attack(self):
		pass
	# 普攻前特殊效果
	def Special_normal_attack(self):
		# 转为真实伤害
		self.champion.attack_attribute.normal_attack.real_damage = self.champion.attack_attribute.normal_attack.physical_damage
		self.champion.attack_attribute.normal_attack.physical_damage = 0
VoidMonster = [[VoidMonster() for _ in range(3)] for _ in range(2)]

# 英雄字典
champion_dic = {1 : Vayne(), 2 : Warwick(), 3 : Ivern(), 4 : Skarner(), 5 : Ashe(), 6 : Alistar(), 7 : Syndra(), 8 : Soraka(), 9 : Renekton(), 10 : Amumu(),\
11 : Rengar(), 12 : Veigar(), 13 : Varus(), 14 : Taric(), 15 : Fizz(), 16 : Nocturne(), 17 : RekSai(), 18 : Olaf(), 19 : Jax(), 20 : Nami(), \
21 : Brand(), 22 : Lux(), 23 : ChoGath(), 24 : Darius(), 25 : Karthus(), 26 : Thresh(), 27 : Katarina(), 28 : Mordekaiser(), 29 : Kindred(), 30 : Azir(), \
31 : Orianna(), 32 : Vladimir(), 33 : Sejuani(), 34 : Kayle(), 35 : Janna(), 36 : KogMaw(), 37 : Cassiopeia(), 38 : Mundo(), 39 : Ornn(), 40 : Aphelios(), \
41 : Graves(), 42 : Yasuo(), 43 : Blitz(), 44 : Yi(), 45 : Shen(), 46 : Akali(), 47 : Kennen(), 48 : Galio(), 49 : Jhin(), 50 : Volibear(), \
51 : Rumble(), 52 : Ziggs(), 53 : Sona(), 54 : Ahri(), 55 : Twisted(), 56 : Caitlyn(), 57 : Leona(), 58 : Fiora(), 59 : Kassadin(), 60 : Lulu(), \
61 : Karma(), 62 : Shyvana(), 63 : Lucian(), 64 : Xerath(), 65 : Ekko(), 66 : Ezreal(), 67 : AurelionSol(), 68 : KhaZix(), 69 : Jinx(), 70 : Annie(), \
71 : Poppy(), 72 :ZhaoXin(), 73 : Heimerdinger()}

# 背景界面
def Sky(screen,finish):
	# 背景(表示天色，魔腾放技能时会变黑)
	if finish:
		sky_color[0] = black
	sky_rect = [[0,0,560,850],[560,0,80,10],[560,40,80,810],[640,0,560,850]]
	for i in range(4):
		pygame.draw.rect(screen,sky_color[0],sky_rect[i],0)

# 英雄界面
class Champion_Interface(object):
	def __init__(self, screen = None, champion = None, game = None): 
		self.screen = screen
		self.champion = champion
		self.game = game
		# 根据位置确定基础点
		if self.champion.position  == 0:
			self.base_x = 277
		elif self.champion.position  == 1:
			self.base_x = 675
		self.base_y = [0,0,0]
		# 英雄图片
		for i in range(3):
			self.base_y[i] = 50+230*i
		if self.champion.champion.name in ('Thresh','ChoGath') and version[0] == 2:
			self.champion_pic = pygame.image.load('pic/Champion/%s/%s2.png' % (self.champion.champion.name,self.champion.champion.name))
		elif self.champion.champion.name in ('Yasuo','Soraka','Fizz','Yi','Shen') and version[0] == 3:
			self.champion_pic = pygame.image.load('pic/Champion/%s/%s3.png' % (self.champion.champion.name,self.champion.champion.name))
		else:
			self.champion_pic = pygame.image.load('pic/Champion/%s/%s.png' % (self.champion.champion.name,self.champion.champion.name))
		# 行动栏图标
		#	死亡
		self.death_pic = pygame.image.load('pic/stat/death.png')
		#	普通普攻
		self.normal_attack_pic = pygame.image.load('pic/stat/normal.png')
		#	普攻暴击且没被闪避
		self.crit_attack_pic = pygame.image.load('pic/stat/crit.png')
		#	普攻被闪避
		self.miss_attack_pic = pygame.image.load('pic/stat/miss.png')
		#	缴械
		self.disarm_pic = pygame.image.load('pic/stat/disarm.png')
		#	stop
		self.stop_pic = pygame.image.load('pic/stat/stop.png')
		#	装弹
		self.load_pic = pygame.image.load('pic/Champion/Jhin/装弹.png')	  
		self.cast_spell_time_count = Time_count()
		wtc = [Time_count() for _ in range(25)]
		self.weapon_time_count = {'领主之刃' : wtc[0], '珠光拳套' : wtc[1], '离子火花' : wtc[2], '幻影之舞' : wtc[3], '卢登回声' : wtc[4], '天使之拥' : wtc[5], \
		'巨石板甲' : wtc[6], '冰脉护手' : wtc[7], '死亡秘典' : wtc[8], '无尽之刃' : wtc[9], '狂热电刀' : wtc[10], '炽热香炉' : wtc[11], '极地战锤' : wtc[12], \
		'飞升护符' : wtc[13], '神臂之弓' : wtc[14], '清风之灵' : wtc[15], '水银披风' : wtc[16], '雷霆劫掠' : wtc[17], '荣光凯旋' : wtc[18], '樱手里剑' : wtc[19], \
		'爆破炸弹' : wtc[20], '魅惑挂坠' : wtc[21], '静止法衣' : wtc[22], '淬炼勋章' : wtc[23], '黑暗之心' : wtc[24]}
		self.get_weapon = [False,False,False]
		self.weapon_rect = [None,None,None]   # 第三个是合成装
		self.weapon_pic = [None,None,None]
		self.para_pic = [[None for _ in range(4)] for _ in range(3)]
		self.rela_pic = [[None,None] for _ in range(r_num[0])]
		para = [['AD','攻速','生命偷取','法强'],['护甲','魔抗','韧性','闪避率'],['穿甲','法穿','暴击率','暴击伤害']]
		for i in range(3):
			for j in range(4):
				self.para_pic[i][j] = pygame.image.load('pic/para/%s.png' % (para[i][j]))
		for ri in range(r_num[0]):
			self.rela_pic[ri][0] = pygame.image.load('pic/rela/%s.png' % r_dic.get(ri+1))
			if r_dic.get(ri+1) in ('极地', '森林', '海洋', '掠食者', '游侠', '钢铁', '水晶','狂战士','地狱火','黯焰','银月','剧毒','雷霆','枪手','忍者','忍剑士',\
				'未来战士', '星之守护者', '爆破专家','奥德赛','源计划','银河机神','护卫','暗星'):
				self.rela_pic[ri][1] = pygame.image.load('pic/rela/%sc.png' % r_dic.get(ri+1))
		rtc = [Time_count() for _ in range(21)] 
		self.rela_time_count = {'极地' : rtc[0], '森林' : rtc[1], '海洋' : rtc[2], '掠食者' : rtc[3], '游侠' : rtc[4], '钢铁' : rtc[5], \
		'水晶' : rtc[6], '狂战士' : rtc[7], '地狱火' : rtc[8], '黯焰' : rtc[9], '银月' : rtc[10], '剧毒' : rtc[11], '雷霆' : rtc[12], \
		'枪手' : rtc[13], '爆破专家' : rtc[14], '奥德赛' : rtc[15], '星之守护者' : rtc[16], '未来战士' : rtc[17], '源计划' : rtc[18], \
		'银河机神' : rtc[19], '护卫' : rtc[20]}
		etc = [Time_count() for _ in range(38)]
		self.effect_time_count = {'祈愿' : etc[0], '冲击之潮' : etc[1], '烈焰风暴' : etc[2], '曲光屏障' : etc[3],'狂热电刀' : etc[4], \
		'离子火花' : etc[5], '卢登回声' : etc[6], '冰脉护手' : etc[7], '光之祭献' : etc[8], '魂引之灯' : etc[9], '羊灵生息' : etc[10], \
		'沙兵攻击' : etc[11], '安魂曲' : etc[12], '魔偶攻击' : etc[13], '月光' : etc[14], '净化剑刃' : etc[15], '活体大炮' : etc[16], \
		'来自艾卡西亚的惊喜' : etc[17], '落雷' : etc[18], '荧焰' : etc[19], '飞轮' :etc[20], '月之驻灵' : etc[21], '天雷' : etc[22], \
		'提伯斯攻击' : etc[23], '欺诈宝珠' : etc[24], '金色卡牌' : etc[25], '红色卡牌' : etc[26], '蓝色卡牌' : etc[27], '时间' : etc[28], \
		'皮克斯攻击' : etc[29], '陨星' : etc[30], '轰炸' : etc[31], '鱼骨头' : etc[32], '圆盾' : etc[33], '炮台攻击' : etc[34], \
		'古灵精怪' : etc[35], '死亡祭献' : etc[36], '闪电链' : etc[37]}
		self.sign_describe_dic = {'千珏之印' : ['千珏之印：在开局时，千珏会随机标','记一个敌人，若千珏成功击杀该目标，','则提升20AD、25%攻速、30%法强'],\
		'雷缚印' : ['雷缚印：凯南的技能与凯南的雷霆羁','绊引起的落雷会给目标叠加1层雷缚印','标记，达到3层时会眩晕目标1.5s'], \
		'孤立无援' : ['孤立无援：该单位处于孤立无援状态，','卡兹克的技能被对该单位造成2倍伤害']}
		esct = [Time_count() for _ in range(20)]
		self.extra_skill_time_count = {'超凡邪力' : esct[0],'复仇之欲' : esct[1],'黑暗庇护' : esct[2],'火焰烙印' : esct[3], '肉食者' : esct[4], \
		'地狱诅咒' : esct[5],'卓尔不凡' : esct[6],'指令_移动' : esct[7], '精怪' : esct[8], '双生毒牙' : esct[9], '冰霜射击' : esct[10], \
		'清辉夜凝' : esct[11], '风之障壁' : esct[12], '曲光屏障' : esct[13], '能量屏障' : esct[14], '双重打击' : esct[15], '忍法！气合盾' : esct[16], \
		'我流忍法！潜龙印' : esct[17],'星神伙伴皮克斯' : esct[18],'龙族血统' : esct[19]}
		# 枪手额外攻击弹道清除计数
		self.clean_count = [[Time_count(),Time_count()],0.5]
		# 炮台镭射轨道清除计数
		self.clean_count2 = [[Time_count(),0.5] for _ in range(3)]
		self.thunder_sign_count = [Time_count(), 0.7]
	# 绘制底图、死者领域、赐福之土、血红之池、护体毒雾、天雷、赛博屏障、银河魔龙、古灵精怪、挑战
	def Bg(self):
		# 环境框
		env_rect = self.base_x-4, self.base_y[self.champion.pos_num]-4, 249+8, 150+8
		#	死者领域
		if self.champion.flag.special_flag.dead_area[0]:
			pygame.draw.rect(self.screen,dark_green2,env_rect,0)
		#	赐福之土
		if self.champion.flag.special_flag.bless_land[0]:
			pygame.draw.rect(self.screen,yellow,env_rect,0)
		# 	血红之池
		if self.champion.flag.special_flag.blood_pool[0]:
			pygame.draw.rect(self.screen,red2,env_rect,0)
		#	护体毒雾
		elif self.champion.flag.special_flag.toxic_smog:
			pygame.draw.rect(self.screen,green3,env_rect,0)
		#	天雷
		elif self.champion.flag.special_flag.thunderbolt:
			pygame.draw.rect(self.screen,(255, 243, 167),env_rect,0)
		#	赛博屏障
		elif self.champion.flag.special_flag.parclose_flag:
			pygame.draw.rect(self.screen,orange,env_rect,0)
		#	魔龙形态
		elif self.champion.champion.name == 'Shyvana':
			if self.champion.champion.skill.para[3][4]:
				dragon_pic = pygame.image.load('pic/Champion/Shyvana/魔龙形态%d.png' % self.champion.position)
				self.screen.blit(dragon_pic,(self.base_x-4, self.base_y[self.champion.pos_num]-4))
		# 	古灵精怪
		elif self.champion.flag.special_flag.odd[0]:
			pygame.draw.rect(self.screen,gray_blue,env_rect,0)
		#	挑战
		elif self.champion.flag.special_flag.challenge[0]:
			pygame.draw.rect(self.screen,yellow,env_rect,0)
		# 外框
		bg_rect = self.base_x, self.base_y[self.champion.pos_num], 249, 150
		pygame.draw.rect(self.screen,gray,bg_rect,0)
		# 英雄图片
		self.screen.blit(self.champion_pic,(self.base_x+16, self.base_y[self.champion.pos_num]+48))
		# 技能圆框
		skill_c = self.base_x+16, self.base_y[self.champion.pos_num]+125
		if self.champion.champion.name == 'Vladimir':
			if self.champion.champion.skill.para[1][0] == 2:
				pygame.draw.circle(self.screen,red2,skill_c,14,0)
			else:
				pygame.draw.circle(self.screen,gray,skill_c,14,0)
		elif self.champion.champion.name == 'Yi':
			if self.champion.champion.skill.para[4][0]:
				pygame.draw.circle(self.screen,purple,skill_c,14,0)
			else:
				pygame.draw.circle(self.screen,gray,skill_c,14,0)
		elif self.champion.champion.name == 'Jhin':
			skill_bg_pic = pygame.image.load('pic/Champion/Jhin/低语%d.png' % self.champion.champion.attack_attribute.attack_count)
			self.screen.blit(skill_bg_pic,(self.base_x+16-14, self.base_y[self.champion.pos_num]+125-14))
		elif self.champion.champion.name == 'Vayne':
			skill_bg_pic = pygame.image.load('pic/Champion/Vayne/圣银弩箭%d.png' % self.champion.champion.attack_attribute.attack_count)
			self.screen.blit(skill_bg_pic,(self.base_x+16-14, self.base_y[self.champion.pos_num]+125-14))
		elif self.champion.champion.name == 'Varus':
			skill_bg_pic = pygame.image.load('pic/Champion/Varus/枯萎箭袋%d.png' % self.champion.champion.attack_attribute.attack_count)
			self.screen.blit(skill_bg_pic,(self.base_x+16-14, self.base_y[self.champion.pos_num]+125-14))
		elif self.champion.champion.name == 'Olaf':
			if self.champion.champion.skill.para[2]:
				pygame.draw.circle(self.screen,red,skill_c,14,0)
			else:
				pygame.draw.circle(self.screen,gray,skill_c,14,0)
		elif self.champion.champion.name == 'Twisted':
			if self.champion.champion.skill.para[2]:
				pygame.draw.circle(self.screen,white,skill_c,14,0)
			else:
				pygame.draw.circle(self.screen,gray,skill_c,14,0)
		elif self.champion.champion.name == 'Yasuo':
			if self.champion.champion.skill.para[0] == 1:
				skill_bg_pic = pygame.image.load('pic/Champion/Yasuo/斩钢闪1.png')
				self.screen.blit(skill_bg_pic,(self.base_x+16-14, self.base_y[self.champion.pos_num]+125-14))
			else:
				pygame.draw.circle(self.screen,gray,skill_c,14,0)
		elif self.champion.champion.name == 'Volibear':
			if self.champion.champion.skill.para[2][1]:
				pygame.draw.circle(self.screen,red,skill_c,14,0)
			elif self.champion.champion.skill.para[2][0]:
				pygame.draw.circle(self.screen,white,skill_c,14,0)
			else:
				pygame.draw.circle(self.screen,gray,skill_c,14,0)
		else:
			pygame.draw.circle(self.screen,gray,skill_c,14,0)
		# 技能图标
		if self.champion.champion.skill.comb[0]:
			self.skill_pic = pygame.image.load('pic/Champion/%s/%s.png' % (self.champion.champion.name,self.champion.champion.skill.name[self.champion.champion.skill.comb[1]]))
			self.cast_spell_pic = pygame.image.load('pic/Champion/%s/%sspell.png' % (self.champion.champion.name,self.champion.champion.skill.name[self.champion.champion.skill.comb[2]]))
		else:
			if self.champion.champion.name in ('Thresh') and version[0] == 2:
				self.skill_pic = pygame.image.load('pic/Champion/%s/%s2.png' % (self.champion.champion.name,self.champion.champion.skill.name))
				self.cast_spell_pic = pygame.image.load('pic/Champion/%s/%sspell2.png' % (self.champion.champion.name,self.champion.champion.skill.name))
			else:
				self.skill_pic = pygame.image.load('pic/Champion/%s/%s.png' % (self.champion.champion.name,self.champion.champion.skill.name))
				if self.champion.champion.name in ('Aphelios','Yasuo','Akali','Twisted','Annie','Heimerdinger') and self.champion.flag.move_flag.show_cast_spell[0]:
					self.cast_spell_pic = pygame.image.load('pic/Champion/%s/%sspell.png' % (self.champion.champion.name,self.champion.flag.move_flag.show_cast_spell[2]))
				else:
					self.cast_spell_pic = pygame.image.load('pic/Champion/%s/%sspell.png' % (self.champion.champion.name,self.champion.champion.skill.name))
		if self.champion.champion.skill.comb[0]:
			self.skill_pic = pygame.image.load('pic/Champion/%s/%s.png' % (self.champion.champion.name,self.champion.champion.skill.name[self.champion.champion.skill.comb[1]]))
		self.screen.blit(self.skill_pic,(self.base_x+5, self.base_y[self.champion.pos_num]+114))
		# 武器栏
		for i in range(2):
			self.weapon_rect[i] = self.base_x+175+21*i, self.base_y[self.champion.pos_num]+28, 17, 17
			pygame.draw.rect(self.screen,black,self.weapon_rect[i],0)
		self.weapon_rect[2] = self.base_x+184,self.base_y[self.champion.pos_num]+5, 20, 20
		pygame.draw.rect(self.screen,black,self.weapon_rect[2],0)
	# 英雄名字与武器状态显示
	def Name(self):
		# 武器状态边框：伏击之爪、朔极之矛、神圣救赎、领主之刃、珠光拳套、离子火花、幻影之舞、卢登回声、水银披风、巨龙之牙、天使之拥、
		# 巨石板甲、冰脉护手、死亡秘典、无尽之刃、狂热电刀、守护天使&巫师法帽、炽热香炉、极地战锤、飞升护符、泰坦坚决、神臂之弓、
		# 夜袭暮刃、清风之灵、雷霆劫掠、荣光凯旋、暗影核心、爆破炸弹、夜之锋刃、魅惑挂坠、淬炼勋章、黑暗之心、圣银胸甲
		s_condition_rect = self.base_x+14,self.base_y[self.champion.pos_num]+6,82,20
		s_condition_color = gray
		if self.champion.flag.weapon_flag.fjzz[0] and self.champion.flag.weapon_flag.fjzz[1]:
			s_condition_color = dark_purple
		elif self.champion.flag.weapon_flag.sjzm[1]:
			s_condition_color = light_green
		elif self.champion.flag.weapon_flag.ssjs[0] and self.champion.flag.weapon_flag.ssjs[1] and not self.champion.flag.weapon_flag.ssjs[4][0]:
			s_condition_color = green
		elif self.champion.flag.weapon_flag.ssjs[4][0]:
			s_condition_color = light_green2
		elif self.champion.flag.weapon_flag.lzzr[2]:
			s_condition_color = orange
			end_flag = self.weapon_time_count['领主之刃'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.lzzr[2] = False
		elif self.champion.flag.weapon_flag.zgqt[2]:
			s_condition_color = dark_pink
			end_flag = self.weapon_time_count['珠光拳套'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.zgqt[2] = False
		elif self.champion.flag.weapon_flag.lzhh[1]:
			s_condition_color = blue2
			end_flag = self.weapon_time_count['离子火花'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.lzhh[1] = False
		elif self.champion.flag.weapon_flag.hyzw[1]:
			s_condition_color = dark_green
			end_flag = self.weapon_time_count['幻影之舞'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.hyzw[1] = False
		elif self.champion.flag.weapon_flag.ldhs[2]:
			s_condition_color = purple
			end_flag = self.weapon_time_count['卢登回声'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.ldhs[2] = False
		elif self.champion.flag.weapon_flag.sypf[2]:
			s_condition_color = cyan
			end_flag = self.weapon_time_count['水银披风'].Duration(30)
			if end_flag:
				self.champion.flag.weapon_flag.sypf[2] = False
		elif self.champion.flag.weapon_flag.jlzy[0]:
			s_condition_color = dark_red
		elif self.champion.flag.weapon_flag.tszy[1]:
			s_condition_color = gray_blue
			end_flag = self.weapon_time_count['天使之拥'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.tszy[1] = False
		elif self.champion.flag.weapon_flag.jsbj[4]:
			s_condition_color = gray_orange
			end_flag = self.weapon_time_count['巨石板甲'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.jsbj[4] = False
		elif self.champion.flag.weapon_flag.bmhs[2]:
			s_condition_color = dark_blue
			end_flag = self.weapon_time_count['冰脉护手'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.bmhs[2] = False
		elif self.champion.flag.weapon_flag.swmd[2]:
			s_condition_color = (40, 31, 61)
			end_flag = self.weapon_time_count['死亡秘典'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.swmd[2] = False
		elif self.champion.flag.weapon_flag.wjzr[2]:
			s_condition_color = dark_yellow
			end_flag = self.weapon_time_count['无尽之刃'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.wjzr[2] = False
		elif self.champion.flag.weapon_flag.krdd[3]:
			s_condition_color = orange_yellow
			end_flag = self.weapon_time_count['狂热电刀'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.krdd[3] = False
		elif self.champion.flag.weapon_flag.shts[1] or self.champion.flag.weapon_flag.wsfm[2][0]:
			s_condition_color = dark_gray
		elif self.champion.flag.weapon_flag.shts[2] or self.champion.flag.weapon_flag.wsfm[3]:
			s_condition_color = light_gray
		elif  self.champion.flag.weapon_flag.crxl[3]:
			s_condition_color = red
			end_flag = self.weapon_time_count['炽热香炉'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.crxl[3] = False
		elif  self.champion.flag.weapon_flag.jdzc[2]:
			s_condition_color = light_blue
			end_flag = self.weapon_time_count['极地战锤'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.jdzc[2] = False
		elif self.champion.flag.weapon_flag.fshf[2]:
			s_condition_color = yellow
			end_flag = self.weapon_time_count['飞升护符'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.fshf[2] = False
		elif self.champion.flag.weapon_flag.ttjj[3]:
			s_condition_color = dark_orange
		elif self.champion.flag.weapon_flag.bbrz[0] and not self.champion.flag.condition_flag.death_flag:
			s_condition_color = orange_red
		elif self.champion.flag.weapon_flag.sbzg[2]:
			s_condition_color = light_cyan
			end_flag = self.weapon_time_count['神臂之弓'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.sbzg[2] = False
		elif self.champion.flag.weapon_flag.yxmr[2]:
			s_condition_color = dark_red2
		elif self.champion.flag.weapon_flag.qfzl[2]:
			s_condition_color = white_green
			end_flag = self.weapon_time_count['清风之灵'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.qfzl[2] = False
		elif self.champion.flag.weapon_flag.ltjl[3]:
			s_condition_color = light_yellow
			end_flag = self.weapon_time_count['雷霆劫掠'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.ltjl[3] = False
		elif self.champion.flag.weapon_flag.ltjl[3]:
			s_condition_color = light_yellow
			end_flag = self.weapon_time_count['雷霆劫掠'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.ltjl[3] = False
		elif self.champion.flag.weapon_flag.rgkx[3]:
			s_condition_color = light_red
			end_flag = self.weapon_time_count['荣光凯旋'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.rgkx[3] = False
		elif self.champion.flag.weapon_flag.yslj[3]:
			s_condition_color = pink
			end_flag = self.weapon_time_count['樱手里剑'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.yslj[3] = False
		elif self.champion.flag.weapon_flag.ayhx[1][0]:
			s_condition_color = (49, 2, 120)
		elif self.champion.flag.weapon_flag.bpzd[2]:
			s_condition_color = orange_red
			end_flag = self.weapon_time_count['爆破炸弹'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.bpzd[2] = False
		elif self.champion.flag.weapon_flag.yzfr[2]:
			s_condition_color = (145, 124, 193)
		elif self.champion.flag.weapon_flag.mhgz[2]:
			s_condition_color = pink#(69, 182, 202)
			end_flag = self.weapon_time_count['魅惑挂坠'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.mhgz[2] = False
		elif self.champion.flag.weapon_flag.jzfy[1]:
			s_condition_color = (51, 77, 199)
			end_flag = self.weapon_time_count['静止法衣'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.jzfy[1] = False
		elif self.champion.flag.weapon_flag.clxz[3]:
			s_condition_color = (33, 149, 127)
			end_flag = self.weapon_time_count['淬炼勋章'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.clxz[3] = False
		elif self.champion.flag.weapon_flag.hazx[3]:
			s_condition_color = black
			end_flag = self.weapon_time_count['黑暗之心'].Duration(1)
			if end_flag:
				self.champion.flag.weapon_flag.hazx[3] = False
		elif self.champion.flag.weapon_flag.syxj[3]:
			s_condition_color = silver
		pygame.draw.rect(self.screen,s_condition_color,s_condition_rect,0)
		# 绘制名称栏
		name_rect = self.base_x+16,self.base_y[self.champion.pos_num]+8,78,16
		pygame.draw.rect(self.screen,white,name_rect,0)
		# 名字
		name_text_font = pygame.font.SysFont("黑体",18)
		name_text = name_text_font.render(("%s" % self.champion.champion.name), 1, (0,0,0))
		if self.champion.champion.name == 'Heimerdinger':
			self.screen.blit(name_text,(self.base_x+16, self.base_y[self.champion.pos_num]+10))
		else:
			self.screen.blit(name_text,(self.base_x+19, self.base_y[self.champion.pos_num]+10))
	# 行动栏图标
	def Action(self):
		# 绘制行动栏
		action_c = self.base_x+249, self.base_y[self.champion.pos_num]+25
		if self.champion.flag.rela_flag['剑士'][3]:
			pygame.draw.circle(self.screen,red,action_c,19,0)
		else:
			pygame.draw.circle(self.screen,sky_color[0],action_c,19,0)
		pygame.draw.circle(self.screen,gray,action_c,16,0)
		# 行动图标
		if self.champion.flag.condition_flag.death_flag:
			self.screen.blit(self.death_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
		else:
			# 普攻
			if self.champion.move.current_move == 'normal_attack':
				if self.champion.flag.condition_flag.debuff_disarm_flag:
					self.screen.blit(self.disarm_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
					# 普攻显示计数清零
					self.champion.flag.move_flag.show_normal_attack[3].value = 0
					self.champion.flag.move_flag.show_normal_attack[0] = False
				else:
					if self.champion.flag.move_flag.show_normal_attack[0]:
						end_flag = self.champion.flag.move_flag.show_normal_attack[3].Duration(self.champion.flag.move_flag.show_normal_attack[1])
						if end_flag:
							self.champion.flag.move_flag.show_normal_attack[0] = False
						else:
							# 普通模式
							if self.champion.flag.move_flag.show_normal_attack[2] == 0:
								self.screen.blit(self.normal_attack_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
							# 普攻暴击不被闪避
							elif self.champion.flag.move_flag.show_normal_attack[2] == 1:
								self.screen.blit(self.crit_attack_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
							# 普攻被闪避
							elif self.champion.flag.move_flag.show_normal_attack[2] == 2:
								self.screen.blit(self.miss_attack_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
			# stop
			elif self.champion.move.current_move == 'stop':
				self.screen.blit(self.stop_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
				# 普攻显示计数清零
				self.champion.flag.move_flag.show_normal_attack[3].value = 0
				self.champion.flag.move_flag.show_normal_attack[0] = False
			# 装弹
			elif self.champion.move.current_move == 'load':
				self.screen.blit(self.load_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
			# 施法
			if self.champion.flag.move_flag.show_cast_spell[0]:
				if self.champion.champion.name == 'Ekko':
					self.screen.blit(self.cast_spell_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
					# 普攻显示计数清零
					self.champion.flag.move_flag.show_normal_attack[3].value = 0
					self.champion.flag.move_flag.show_normal_attack[0] = False
				else:
					if not self.champion.flag.special_flag.motionless_flag:
						cast_spell_end_flag = self.cast_spell_time_count.Duration(self.champion.flag.move_flag.show_cast_spell[1])
						# 被打断施法
						if self.champion.champion.skill.continuous[3]:
							cast_spell_end_flag = True
							self.cast_spell_time_count.value = 0
							self.champion.champion.skill.continuous[3] = False
						if cast_spell_end_flag:
							self.champion.flag.move_flag.show_cast_spell[0] = False
							if self.champion.champion.skill.comb[0]:
								self.champion.champion.skill.comb[2] = ~self.champion.champion.skill.comb[2]+2
						else:
							if self.champion.champion.skill.comb[0]:
								self.cast_spell_pic = pygame.image.load('pic/Champion/%s/%sspell.png' % (self.champion.champion.name,self.champion.champion.skill.name[self.champion.champion.skill.comb[2]]))
							self.screen.blit(self.cast_spell_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+9))
							# 普攻显示计数清零
							self.champion.flag.move_flag.show_normal_attack[3].value = 0
							self.champion.flag.move_flag.show_normal_attack[0] = False
	# 绘制血条蓝条
	def Hpmp(self):
		# 血条背景
		hp_bg_rect = self.base_x+16, self.base_y[self.champion.pos_num]+28, 153, 10
		pygame.draw.rect(self.screen,black,hp_bg_rect,0)
		# 血条
		if self.champion.champion.hp.value > 0:
			if self.champion.condition.shield.value > 0:
				if self.champion.champion.hp.value + self.champion.condition.shield.value > self.champion.champion.hp.max_value:
					shield_width = 153
					hp_width = int(153 * (self.champion.champion.hp.value / (self.champion.champion.hp.max_value + self.champion.condition.shield.value)))
				else:
					shield_width = int(153*((self.champion.champion.hp.value + self.champion.condition.shield.value) / self.champion.champion.hp.max_value))
					hp_width = int(153 * (self.champion.champion.hp.value / self.champion.champion.hp.max_value))
				shield_rect = self.base_x+16, self.base_y[self.champion.pos_num]+28, shield_width, 10
				pygame.draw.rect(self.screen,white,shield_rect,0)
			else:
				hp_width = int(153 * (self.champion.champion.hp.value / self.champion.champion.hp.max_value))
			hp_rect = self.base_x+16, self.base_y[self.champion.pos_num]+28, hp_width, 10
			color_hp = red
			pygame.draw.rect(self.screen,color_hp,hp_rect,0)
		hp_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 9)
		hp_text = hp_font.render(("%d/%d" % (self.champion.champion.hp.value,self.champion.champion.hp.max_value)), 1, white)
		self.screen.blit(hp_text,(self.base_x+120, self.base_y[self.champion.pos_num]+28))
		# 绘制掠食者斩杀线
		#	判断敌方有无掠食者羁绊
		for i in range(3):
			lsz_n = self.champion.game.LR_rela[~self.champion.position+2]['掠食者']
			if lsz_n > 1:
				deadline = self.base_x+16+rela_dic['掠食者'][1][lsz_n-2]*153, self.base_y[self.champion.pos_num]+28, 1, 10
				pygame.draw.rect(self.screen,black,deadline,0)

		# 蓝条
		# 蓝条背景
		mp_bg_rect = self.base_x+16, self.base_y[self.champion.pos_num]+39, 153, 6
		pygame.draw.rect(self.screen,black,mp_bg_rect,0)
		if self.champion.champion.mp.max_value > 0:
			if self.champion.champion.mp.max_value == 0:
				mp_width = 0
			else:
				mp_width = int(153 * (self.champion.champion.mp.value / self.champion.champion.mp.max_value))
			mp_rect = self.base_x+16, self.base_y[self.champion.pos_num]+39,mp_width,6
			# 忍者使用能量
			if self.champion.flag.special_flag.chakra_flag:
				color_mp = (253, 150, 34)
			else:
				# 沉默
				if self.champion.flag.condition_flag.debuff_silence_flag:
					color_mp = white
				# 中毒
				elif self.champion.flag.condition_flag.debuff_poisoning_flag[0]:
					color_mp = green2
				# 破法
				elif self.champion.flag.condition_flag.debuff_broken_flag:
					color_mp = gray_blue
				else:
					color_mp = blue
			pygame.draw.rect(self.screen,color_mp,mp_rect,0)
	# 厄斐琉斯飞轮
	def Chakram(self,Aphelios):
		Chakram_pic = pygame.image.load('pic/Champion/Aphelios/飞轮.png')
		for i in range(Aphelios.mwd_dic['折镜'][2][2]):
			self.screen.blit(Chakram_pic,(self.base_x+9+20*i, self.base_y[Aphelios.pos_num]+154))
	# 绘制武器栏、千珏之印、雷缚印、孤立无援标记、清辉标记、夜凝标记、日光标记、龙血标记
	def Weapon(self,pos_mouse):
		# 基础武器
		for i in range(2):
			if (self.champion.weapon.weapon[i]) != None:
				self.weapon_pic[i] = pygame.image.load('pic/weapon/%s.png' % self.champion.weapon.weapon[i])
				self.screen.blit(self.weapon_pic[i],(self.base_x+175+21*i, self.base_y[self.champion.pos_num]+28))
				self.get_weapon[i] = True
		# 进阶武器
		if self.champion.weapon.weapon[1] != None:
			self.weapon_pic[2] = pygame.image.load('pic/weapon/%s.png' % self.champion.weapon.weapon[2])
			self.screen.blit(self.weapon_pic[2],(self.base_x+184, self.base_y[self.champion.pos_num]+5))
			self.get_weapon[2] = True
		# 标记
		sign_name = None
		if self.champion.flag.special_flag.Kindred_sign:
			sign_name = '千珏之印'
			sign_pic = pygame.image.load('pic/champion/Kindred/千珏之印标记.png')
			self.screen.blit(sign_pic,(self.base_x+209, self.base_y[self.champion.pos_num]+7))
		elif self.champion.flag.special_flag.thunder_sign > 0:
			sign_name = '雷缚印'
			if self.champion.flag.special_flag.thunder_sign < 3:
				sign_pic = pygame.image.load('pic/champion/Kennen/雷缚印%d.png' % self.champion.flag.special_flag.thunder_sign)
				self.screen.blit(sign_pic,(self.base_x+209, self.base_y[self.champion.pos_num]+7))
			else:
				end_flag = self.thunder_sign_count[0].Duration(self.thunder_sign_count[1])
				if end_flag:
					self.champion.flag.special_flag.thunder_sign = 0
				else:
					sign_pic = pygame.image.load('pic/champion/Kennen/雷缚印3.png')
					self.screen.blit(sign_pic,(self.base_x+209, self.base_y[self.champion.pos_num]+7))
		elif self.champion.flag.special_flag.ooal_sign:
			sign_name = '孤立无援'
			sign_pic = pygame.image.load('pic/champion/KhaZix/孤立无援.png')
			self.screen.blit(sign_pic,(self.base_x+209, self.base_y[self.champion.pos_num]+7))
		# 厄斐琉斯标记：清灰、夜凝
		for i in range(2):
			Aphelios_sign_bg_c = self.base_x+175+21+26, self.base_y[self.champion.pos_num]+31+11*i
			pygame.draw.circle(self.screen,gray,Aphelios_sign_bg_c,3,0)
		As_num = 0
		# 清辉标记
		if self.champion.flag.special_flag.qh_sign:
			qh_sign_c =  self.base_x+175+21+26, self.base_y[self.champion.pos_num]+31
			pygame.draw.circle(self.screen,light_green,qh_sign_c,3,0)
			As_num += 1
		# 夜凝标记
		if self.champion.flag.special_flag.yn_sign:
			yn_sign_c =  self.base_x+175+21+26, self.base_y[self.champion.pos_num]+31+11*As_num
			pygame.draw.circle(self.screen,dark_purple,yn_sign_c,3,0)
		# 日光标记
		if self.champion.flag.special_flag.sunlight_sign[0]:
			rg_sign_c =  self.base_x+175+21+26, self.base_y[self.champion.pos_num]+31+11*As_num
			pygame.draw.circle(self.screen,orange,rg_sign_c,3,0)
			As_num += 1
		# 龙血标记
		if self.champion.flag.special_flag.dragon_sign:
			rg_sign_c =  self.base_x+175+21+26, self.base_y[self.champion.pos_num]+31+11*As_num
			pygame.draw.circle(self.screen,red,rg_sign_c,3,0)
		# 进阶武器效果描述
		weapon_func_rect = self.base_x, self.base_y[self.champion.pos_num]+155, 249, 70
		weapon_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 14)
		if self.get_weapon[2]:
			if self.base_x+184<=pos_mouse[0]<=self.base_x+184+20 and self.base_y[self.champion.pos_num]+5<=pos_mouse[1]<=self.base_y[self.champion.pos_num]+2+20:
				pygame.draw.rect(self.screen,gray,weapon_func_rect,0)
				wp_des_len = len(advance_weapon[self.champion.weapon.weapon[2]])
				for i in range(wp_des_len):
					weapon_text = weapon_font.render(("%s" % advance_weapon[self.champion.weapon.weapon[2]][i]),1,(0,0,0))
					if self.champion.weapon.weapon[2] == '窃贼手套' and i >= 1:
						weapon_text = weapon_font.render(("偷到：%s" % self.champion.weapon.weapon[i+2]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '分裂飓风' and i == 3:
						weapon_text = weapon_font.render(("%s" % self.champion.flag.weapon_flag.fljf[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '领主之刃' and i == 3:
						weapon_text = weapon_font.render(("层数：%d" % self.champion.flag.weapon_flag.lzzr[1]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '巨石板甲' and i == 3:
						weapon_text = weapon_font.render(("层数：%d" % self.champion.flag.weapon_flag.jsbj[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '幻影之舞' and i == 2:
						weapon_text = weapon_font.render(("闪避暴击次数：%d" % self.champion.flag.weapon_flag.hyzw[2]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '鬼索之怒' and i == 1:
						weapon_text = weapon_font.render(("层数：%d" % self.champion.flag.weapon_flag.gszn[2]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '冰脉护手' and i == 3:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.bmhs[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '沉默匕首' and i == 3:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.cmbs[2]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '正义之手' and i >= 2:
						t = ['增伤','回血']
						weapon_text = weapon_font.render(("触发%s次数：%d" % (t[i-2],self.champion.flag.weapon_flag.zyzs[3][i-2])),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '折戟秘刀' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.zjmd[2]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '珠光拳套' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.zgqt[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '离子火花' and i == 3:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.lzhh[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '狂热电刀' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.krdd[4]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '卑劣手斧' and i == 2:
						weapon_text = weapon_font.render(("累计护盾值：%d" % self.champion.flag.weapon_flag.blsf[2]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '极地战锤' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.jdzc[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '飞升护符' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.fshf[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '泰坦坚决' and i == 3:
						weapon_text = weapon_font.render(("层数：%d" % self.champion.flag.weapon_flag.ttjj[1][0]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '神臂之弓' and i == 3:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.sbzg[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '清风之灵' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.qfzl[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '雷霆劫掠' and i == 3:
						weapon_text = weapon_font.render(("触发震击次数：%d" % self.champion.flag.weapon_flag.ltjl[4]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '荣光凯旋' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.rgkx[4]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '樱手里剑' and i == 3:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.yslj[4]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '爆破炸弹' and i == 2:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.bpzd[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '夜之锋刃' and i == 3:
						weapon_text = weapon_font.render(("格挡技能次数：%d" % self.champion.flag.weapon_flag.yzfr[4]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '魅惑挂坠' and i == 3:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.mhgz[3]),1,(0,0,0))
					elif self.champion.weapon.weapon[2] == '黑暗之心' and i == 3:
						weapon_text = weapon_font.render(("触发次数：%d" % self.champion.flag.weapon_flag.hazx[4]),1,(0,0,0))
					self.screen.blit(weapon_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
					# 特殊机制介绍
					if self.champion.weapon.weapon[2] == '雷霆劫掠':
						self.Special_mechanism_description('感电状态')
					elif self.champion.weapon.weapon[2] in ('凡性提醒','死亡秘典','荆棘之甲','荆棘之咬'):
						self.Special_mechanism_description('重伤状态')
					elif self.champion.weapon.weapon[2] == '静止法衣':
						self.Special_mechanism_description('破法状态')
		# 基础武器描述
		#	第一个基础武器
		if self.base_x+175<=pos_mouse[0]<=self.base_x+175+17 and self.base_y[self.champion.pos_num]+28<=pos_mouse[1]<=self.base_y[self.champion.pos_num]+28+17\
		and self.champion.weapon.weapon[0] != None:
			pygame.draw.rect(self.screen,gray,weapon_func_rect,0)
			if self.champion.flag.rela_flag['源计划'][0]:
				bw1_text = weapon_font.render(("%s" % basic_weapon_describe[self.champion.weapon.weapon[0]][self.champion.flag.rela_flag['源计划'][3]-1]),1,(0,0,0))
			else:
				bw1_text = weapon_font.render(("%s" % basic_weapon_describe[self.champion.weapon.weapon[0]][0]),1,(0,0,0))
			self.screen.blit(bw1_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159))
		#	第二个基础装备
		if self.base_x+175+21<=pos_mouse[0]<=self.base_x+175+21+17 and self.base_y[self.champion.pos_num]+28<=pos_mouse[1]<=self.base_y[self.champion.pos_num]+28+17\
		and self.champion.weapon.weapon[1] != None:
			pygame.draw.rect(self.screen,gray,weapon_func_rect,0)
			if self.champion.flag.rela_flag['源计划'][0]:
				bw2_text = weapon_font.render(("%s" % basic_weapon_describe[self.champion.weapon.weapon[1]][self.champion.flag.rela_flag['源计划'][3]-1]),1,(0,0,0))
			else:
				bw2_text = weapon_font.render(("%s" % basic_weapon_describe[self.champion.weapon.weapon[1]][0]),1,(0,0,0))
			self.screen.blit(bw2_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159))
		# 标记描述
		if sign_name != None:
			sign_rect = self.base_x, self.base_y[self.champion.pos_num]+155, 249, 70
			d = ((pos_mouse[0]-(self.base_x+217))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+15))**2)
			if d <= 64:
				pygame.draw.rect(self.screen,gray,sign_rect,0)
				sign_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 14)
				des_len = len(self.sign_describe_dic[sign_name])
				for i in range(des_len):
					sign_text = sign_font.render(('%s' % self.sign_describe_dic[sign_name][i]), 1, (0,0,0))
					self.screen.blit(sign_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
	# 绘制状态栏：依次是眩晕、冰冻、减伤、重伤、无敌、不可阻挡、魔法护盾、不可选取、炽热、钢铁、灼烧、剧毒、感电、完全闪避、压制、时间静止
	def Condition(self):
		for i in range(4):
			condition_bg_c = self.base_x+108+18*i, self.base_y[self.champion.pos_num]+16
			pygame.draw.circle(self.screen,gray,condition_bg_c,6,0)
		condition = [[self.champion.flag.condition_flag.debuff_dizz_flag,purple],[self.champion.flag.condition_flag.debuff_frozen_flag,light_blue],\
		[self.champion.flag.condition_flag.buff_matigation_flag,orange],[self.champion.flag.condition_flag.debuff_injury_flag,black],\
		[self.champion.flag.condition_flag.buff_invincible_flag,yellow],[self.champion.flag.condition_flag.buff_unstoppable_flag,dark_purple],\
		[self.champion.flag.condition_flag.buff_magic_shield_flag,gray_blue],[self.champion.flag.condition_flag.miss_flag[0],white],\
		[self.champion.flag.condition_flag.buff_fervor_flag,red],[self.champion.flag.condition_flag.buff_iron_flag[0],dark_gray],\
		[self.champion.flag.condition_flag.debuff_burn_flag,orange_red],[self.champion.flag.condition_flag.debuff_poisoning_flag[0],green2],\
		[self.champion.flag.condition_flag.debuff_electrification_flag,blue],\
		[(self.champion.champion.defensive_attribute.dodge_mechanism.all_dodge[2] or self.champion.champion.defensive_attribute.dodge_mechanism.all_dodge[0]),white_green],\
		[self.champion.flag.condition_flag.suppress[0],dark_red],[self.champion.flag.special_flag.motionless_flag,(66, 201, 246)]]
		condition_number = 0
		for i in range(len(condition)):
			if condition[i][0]:
				condition_c = self.base_x+108+18*condition_number, self.base_y[self.champion.pos_num]+16
				pygame.draw.circle(self.screen,condition[i][1],condition_c,6,0)
				condition_number += 1
	# 绘制攻击对象（enemy）头像
	def Enemy(self):
		enemy_c = self.base_x+249, self.base_y[self.champion.pos_num]+125
		if self.champion.flag.condition_flag.debuff_taunt_flag or self.champion.flag.special_flag.challenge[2]:
			pygame.draw.circle(self.screen,red,enemy_c,19,0)
		else:
			pygame.draw.circle(self.screen,sky_color[0],enemy_c,19,0)
		pygame.draw.circle(self.screen,gray,enemy_c,16,0)
		# 敌人头像
		if (not self.champion.flag.condition_flag.death_flag):
			if self.champion.enemy.champion.name in ('Thresh','ChoGath') and version[0] == 2:
				self.enemy_pic = pygame.image.load('pic/Champion/%s/%s_h2.png' % (self.champion.enemy.champion.name,self.champion.enemy.champion.name))
			elif self.champion.enemy.champion.name in ('Yasuo','Soraka','Fizz','Yi','Shen') and version[0] == 3:
				self.enemy_pic = pygame.image.load('pic/Champion/%s/%s_h3.png' % (self.champion.enemy.champion.name,self.champion.enemy.champion.name))
			else:
				self.enemy_pic = pygame.image.load('pic/Champion/%s/%s_h.png' % (self.champion.enemy.champion.name,self.champion.enemy.champion.name))
			self.screen.blit(self.enemy_pic,(self.base_x+233, self.base_y[self.champion.pos_num]+109))
	# 显示技能描述、额外技能
	def Skill(self,pos_mouse):
		if self.champion.champion.skill.extra[0]:
			for i in range(self.champion.champion.skill.extra[1]):
				skill_extra_c = self.base_x+46+29*i, self.base_y[self.champion.pos_num]+125
				if self.champion.champion.skill.extra[2][i][2]:
					if self.champion.champion.skill.extra[2][i][0] in ('水晶之力','野蛮怒吼','正气凌人','恕瑞玛的传承','狂沙猛攻','羊灵生息','千珏之印','终极时刻',\
						'冰霜护甲','来自艾卡西亚的惊喜','星火符刃','工匠大师','巨像重击','摄魂夺魄','梵咒','罪恶快感','坚定风采','升级!!!','挑战','狂雷渐起'):
						skill_extra_color = white
					elif self.champion.champion.skill.extra[2][i][0] in ('银河魔龙降世','血红之池'):
						skill_extra_color = red
					elif self.champion.champion.skill.extra[2][i][0] == '古灵':
						skill_extra_color = gray_blue
					else:
						end_flag = self.extra_skill_time_count[self.champion.champion.skill.extra[2][i][0]].Duration(1)
						if end_flag:
							self.champion.champion.skill.extra[2][i][2] = False
							skill_extra_color = gray
						else:
							skill_extra_color = white
				else:
					skill_extra_color = gray
				if self.champion.champion.name == 'Yi' and i == 0 and not self.champion.champion.skill.extra[2][0][2]:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Yi/双重打击%d.png' % self.champion.champion.attack_attribute.attack_count)
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Aphelios' and i <= 1:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Aphelios/子弹%d.png' % self.champion.mwd_dic[self.champion.moon_weapon[self.champion.weapon_seq[i]][0]][0])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46+29*i-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Galio' and i == 0 and not self.champion.champion.skill.extra[2][0][2]:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Galio/巨像重击%d.png' % self.champion.champion.skill.para[3][0])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Twisted' and i == 0:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Twisted/卡牌骗术%d.png' % self.champion.champion.attack_attribute.attack_count)
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Ahri' and i == 0 and not self.champion.champion.skill.extra[2][0][2]:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Ahri/摄魂夺魄%d.png' % self.champion.champion.skill.para[3][0])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Karma' and i == 0 and not self.champion.champion.skill.extra[2][0][2]:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Karma/梵咒%d.png' % self.champion.champion.skill.para[3][0])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Caitlyn' and i == 0:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Caitlyn/爆头%d.png' % self.champion.champion.skill.para[3][0])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Shyvana' and i == 0 and not self.champion.champion.skill.extra[2][0][2]:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Shyvana/怒气%d.png' % self.champion.champion.skill.para[3][2][2])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Heimerdinger' and i == 0 and not self.champion.champion.skill.extra[2][0][2]:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Heimerdinger/升级%d.png' % self.champion.champion.skill.para[2][0])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				elif self.champion.champion.name == 'Volibear' and i == 0 and not self.champion.champion.skill.extra[2][0][2]:
					skill_extra_bg_pic = pygame.image.load('pic/Champion/Volibear/狂雷渐起%d.png' % self.champion.champion.skill.para[3][0])
					self.screen.blit(skill_extra_bg_pic,(self.base_x+46-13, self.base_y[self.champion.pos_num]+125-13))
				else:
					pygame.draw.circle(self.screen,skill_extra_color,skill_extra_c,13,0)
				if self.champion.champion.name in ('Thresh') and version[0] == 2:
					skill_extra_pic = pygame.image.load('pic/Champion/%s/%s2.png' % (self.champion.champion.name,self.champion.champion.skill.extra[2][i][0]))
				else:
					skill_extra_pic = pygame.image.load('pic/Champion/%s/%s.png' % (self.champion.champion.name,self.champion.champion.skill.extra[2][i][0]))
				self.screen.blit(skill_extra_pic,(self.base_x+36+29*i, self.base_y[self.champion.pos_num]+115))
		skill_rect = self.base_x, self.base_y[self.champion.pos_num]+155, 249, 70
		skill_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 14)
		d1 = ((pos_mouse[0]-(self.base_x+16))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+125))**2)
		if d1 <= 121:
			pygame.draw.rect(self.screen,gray,skill_rect,0)
			if self.champion.champion.skill.comb[0]:
				des_len = len(self.champion.champion.skill.describe[self.champion.champion.skill.comb[1]])
				for i in range(des_len):
					skill_text = skill_font.render(('%s' % self.champion.champion.skill.describe[self.champion.champion.skill.comb[1]][i]), 1, (0,0,0))
					self.screen.blit(skill_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
			else:
				des_len = len(self.champion.champion.skill.describe)
				for i in range(des_len):
					skill_text = skill_font.render(('%s' % self.champion.champion.skill.describe[i]), 1, (0,0,0))
					self.screen.blit(skill_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
			# 特殊机制介绍
			if self.champion.champion.skill.name == '雷霆吐息':
				self.Special_mechanism_description('感电状态')
			elif self.champion.champion.skill.name == '无尽束缚':
				self.Special_mechanism_description('压制状态')
			elif self.champion.champion.skill.name == '魔法水晶箭':
				self.Special_mechanism_description('冰冻状态')
			elif self.champion.champion.skill.name == '死亡莲华':
				self.Special_mechanism_description('重伤状态')
			elif self.champion.champion.skill.name in ('坚定意志','遁地','冥想','杜朗护盾','赛博屏障'):
				self.Special_mechanism_description('减伤状态')
			elif self.champion.champion.skill.name in ('纵火盛宴','烈焰吐息(魔龙形态)'):
				self.Special_mechanism_description('灼烧状态')
			elif self.champion.champion.skill.name == '时间干扰脉冲':
				self.Special_mechanism_description('破法状态')
		if self.champion.champion.skill.extra[0]:
			d2 = ((pos_mouse[0]-(self.base_x+46))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+125))**2)
			if d2 <= 100:
				pygame.draw.rect(self.screen,gray,skill_rect,0)
				des_len1 = len(self.champion.champion.skill.extra[2][0][1])
				for i in range(des_len1):
					extra1_text = skill_font.render(('%s' % self.champion.champion.skill.extra[2][0][1][i]), 1, (0,0,0))
					if self.champion.champion.skill.extra[2][0][0] == '超凡邪力' and i == 2:
						extra1_text = skill_font.render(('层数：%d' % self.champion.champion.skill.para[2]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '复仇之欲' and i == 2:
						extra1_text = skill_font.render(('层数：%d' % self.champion.champion.skill.para[3]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '火焰烙印' and i == 2:
						extra1_text = skill_font.render(('触发次数：%d' % self.champion.champion.skill.para[4]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '肉食者' and i == 2:
						extra1_text = skill_font.render(('触发次数：%d' % self.champion.champion.skill.para[4]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '地狱诅咒' and i == 2:
						extra1_text = skill_font.render(('层数：%d' % self.champion.champion.skill.para[4]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '千珏之印' and i == 3 and self.champion.champion.skill.para[6][3]:
						extra1_text = skill_font.render(('已触发'), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '卓尔不凡' and i == 2:
						extra1_text = skill_font.render(('层数：%d' % self.champion.champion.skill.para[3]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '冰霜射击' and i == 2:
						extra1_text = skill_font.render(('触发次数：%d' % self.champion.champion.skill.para[2][2]), 1, (0,0,0))
					elif self.champion.champion.name == 'Aphelios' and i == 3:
						if self.champion.mwd_dic['折镜'][1]:
							extra1_text = skill_font.render(('主武器，剩余子弹：%d；飞轮数：%d' % (self.champion.mwd_dic['折镜'][0],self.champion.mwd_dic['折镜'][2][2])), 1, (0,0,0))
						else:
							extra1_text = skill_font.render(('主武器，剩余子弹：%d' % self.champion.mwd_dic[self.champion.moon_weapon[self.champion.weapon_seq[0]][0]][0]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '能量屏障' and i == 2:
						if self.champion.champion.skill.para[2][0]:
							extra1_text = skill_font.render(('已触发'), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '双重打击' and i == 3:
						extra1_text = skill_font.render(('连续普攻计数：%d' % self.champion.champion.attack_attribute.attack_count), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '忍法！气合盾' and i == 2:
						extra1_text = skill_font.render(('触发次数：%d' % self.champion.champion.skill.para[1][2]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '我流忍法！潜龙印' and i == 3:
						extra1_text = skill_font.render(('触发次数：%d' % self.champion.champion.skill.para[4][4]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '忍法！雷缚印' and i == 3:
						extra1_text = skill_font.render(('触发次数：%d' % self.champion.champion.skill.para[5]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '巨像重击' and i == 3:
						extra1_text = skill_font.render(('触发次数：%d' % self.champion.champion.skill.para[5]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '爆头' and i == 3:
						extra1_text = skill_font.render(('爆头次数：%d' % self.champion.champion.skill.para[3][4]), 1, (0,0,0))
					elif self.champion.champion.skill.extra[2][0][0] == '银河魔龙降世' and i == 3:
						extra1_text = skill_font.render(('怒气：%d/100' % self.champion.champion.skill.para[3][2][0]), 1, (0,0,0))
					self.screen.blit(extra1_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
				if self.champion.champion.skill.extra[2][0][0] == '我流忍法！潜龙印':
					self.Special_mechanism_description('重伤状态')
			if self.champion.champion.skill.extra[1] >= 2:
				d3 = ((pos_mouse[0]-(self.base_x+46+29))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+125))**2)
				if d3 <= 100:
					pygame.draw.rect(self.screen,gray,skill_rect,0)
					des_len1 = len(self.champion.champion.skill.extra[2][1][1])
					for i in range(des_len1):
						extra1_text = skill_font.render(('%s' % self.champion.champion.skill.extra[2][1][1][i]), 1, (0,0,0))
						if self.champion.champion.name == 'Aphelios' and i == 3:
							if self.champion.moon_weapon[self.champion.weapon_seq[1]][0] == '折镜':
								extra1_text = skill_font.render(('副武器，剩余子弹：%d；飞轮数：%d' % (self.champion.mwd_dic['折镜'][0],self.champion.mwd_dic['折镜'][2][2])), 1, (0,0,0))
							else:
								extra1_text = skill_font.render(('副武器，剩余子弹：%d' % self.champion.mwd_dic[self.champion.moon_weapon[self.champion.weapon_seq[1]][0]][0]), 1, (0,0,0))
						self.screen.blit(extra1_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
			if self.champion.champion.skill.extra[1] >= 3:
				d4 = ((pos_mouse[0]-(self.base_x+46+29+29))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+125))**2)
				if d4 <= 100:
					pygame.draw.rect(self.screen,gray,skill_rect,0)
					des_len1 = len(self.champion.champion.skill.extra[2][2][1])
					for i in range(des_len1):
						extra1_text = skill_font.render(('%s' % self.champion.champion.skill.extra[2][2][1][i]), 1, (0,0,0))
						self.screen.blit(extra1_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
			if self.champion.champion.skill.extra[1] >= 4:
				d5 = ((pos_mouse[0]-(self.base_x+46+29+29+29))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+125))**2)
				if d5 <= 100:
					pygame.draw.rect(self.screen,gray,skill_rect,0)
					des_len1 = len(self.champion.champion.skill.extra[2][3][1])
					for i in range(des_len1):
						extra1_text = skill_font.render(('%s' % self.champion.champion.skill.extra[2][3][1][i]), 1, (0,0,0))
						self.screen.blit(extra1_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
	# 显示英雄属性(加总造成伤害、总治疗量、暴击次数、闪避次数，特殊：完全闪避期间闪避次数、触发雷霆羁绊次数)/特殊机制介绍
	def Para(self,pos_mouse):
		if self.champion.position == 0:
			para_rect_x = self.base_x-167-49
			damage_rect_x = para_rect_x
		else:
			para_rect_x = self.base_x+267+5
			damage_rect_x = para_rect_x
		para_rect = para_rect_x, self.base_y[self.champion.pos_num], 157+49, 102
		#pygame.draw.rect(self.screen,sky_color[0],para_rect,0)
		damage_rect = damage_rect_x, self.base_y[self.champion.pos_num]+106, 157+49, 30+14
		#pygame.draw.rect(self.screen,sky_color[0],damage_rect,0)
		# 伤害占比颜色显示
		damage_color_rect = damage_rect_x + 6, self.base_y[self.champion.pos_num]+106+4, 194, 10
		# 物理/魔法/真实伤害/治疗量
		pd_rect_w = int(self.champion.champion.attack_attribute.all_damage.physical_damage / 1500 * 194)
		sd_rect_w = int(self.champion.champion.attack_attribute.all_damage.spell_damage / 1500 * 194) + pd_rect_w
		rd_rect_w = int(self.champion.champion.attack_attribute.all_damage.real_damage / 1500 * 194) + sd_rect_w
		hd_rect_w = int(self.champion.champion.hp.heal / 1500 * 194) + rd_rect_w
		# 	超出范围折算
		if hd_rect_w > 194:
			k = 194 / hd_rect_w
			hd_rect_w = 194
			rd_rect_w = int(rd_rect_w * k)
			sd_rect_w = int(sd_rect_w * k)
			pd_rect_w = int(pd_rect_w * k)
		pd_rect = damage_rect_x + 6, self.base_y[self.champion.pos_num]+106+4, pd_rect_w, 10
		sd_rect = damage_rect_x + 6, self.base_y[self.champion.pos_num]+106+4, sd_rect_w, 10
		rd_rect = damage_rect_x + 6, self.base_y[self.champion.pos_num]+106+4, rd_rect_w, 10
		hd_rect = damage_rect_x + 6, self.base_y[self.champion.pos_num]+106+4, hd_rect_w, 10
		if  self.base_x+16<=pos_mouse[0]<=self.base_x+16+217 and self.base_y[self.champion.pos_num]+48<=pos_mouse[1]<=self.base_y[self.champion.pos_num]+48+95:
			pygame.draw.rect(self.screen,gray,para_rect,0)
			pygame.draw.rect(self.screen,gray,damage_rect,0)
			pygame.draw.rect(self.screen,black,damage_color_rect,0)
			if hd_rect_w > 0:
				pygame.draw.rect(self.screen,light_green,hd_rect,0)
			if rd_rect_w > 0:
				pygame.draw.rect(self.screen,white,rd_rect,0)
			if sd_rect_w > 0:
				pygame.draw.rect(self.screen,gray_blue,sd_rect,0)
			if pd_rect_w > 0:
				pygame.draw.rect(self.screen,orange,pd_rect,0)
			
			# 显示完全闪避时闪避普攻次数
			if self.champion.champion.defensive_attribute.dodge_mechanism.all_dodge[0]:
				all_dodge_count = '/%d' % self.champion.champion.defensive_attribute.dodge_mechanism.all_dodge[1]
			else:
				all_dodge_count = ''
			# 显示触发雷霆羁绊次数
			if self.champion.flag.rela_flag['雷霆'][0]:
				thunder_count = '/(%d)' % self.champion.champion.relatedness.thunder_number
			else:
				thunder_count = ''
			damage_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 14)
			damage_text = damage_font.render(("%d(%d/%d/%d)/%d/%d/%d%s%s" % (self.champion.champion.attack_attribute.all_damage.total_damage, self.champion.champion.attack_attribute.all_damage.physical_damage, \
				self.champion.champion.attack_attribute.all_damage.spell_damage, self.champion.champion.attack_attribute.all_damage.real_damage, self.champion.champion.hp.heal, \
				self.champion.champion.attack_attribute.crit_mechanism.crit_count, self.champion.champion.defensive_attribute.dodge_mechanism.dodge_count, all_dodge_count, thunder_count)), 1, (0,0,0))
			self.screen.blit(damage_text,(damage_rect_x+6, self.base_y[self.champion.pos_num]+127))
			para_value = [[self.champion.champion.attack_attribute.AD,self.champion.champion.attack_attribute.attack_speed,self.champion.champion.hemophagia,self.champion.champion.attack_attribute.spell_power],\
			[self.champion.champion.defensive_attribute.armor,self.champion.champion.defensive_attribute.spell_resistance,self.champion.champion.defensive_attribute.tenacity,self.champion.champion.defensive_attribute.dodge_mechanism.dodge],\
			[self.champion.champion.attack_attribute.armor_penetration,self.champion.champion.attack_attribute.spell_resistance_penetration,self.champion.champion.attack_attribute.crit_mechanism.crit,self.champion.champion.attack_attribute.crit_mechanism.crit_multiple]]
			para_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 14)
			for i in range(3):
				for j in range(4):
					self.screen.blit(self.para_pic[i][j],(para_rect_x+6+49*j, self.base_y[self.champion.pos_num]+9+33*i))
					if (i == 0 and j == 0) or (i == 1 and j == 0) or (i == 1 and j == 1) or (i == 2 and j == 0) or (i == 2 and j ==1):
						para_text = para_font.render(("%d" % para_value[i][j]), 1, (0,0,0))
					else:
						para_text = para_font.render(("%.2f" % para_value[i][j]), 1, (0,0,0))
					self.screen.blit(para_text,(para_rect_x+26+49*j, self.base_y[self.champion.pos_num]+11+33*i))
	# 特殊机制介绍
	def Special_mechanism_description(self,mechanism):
		description = {'能量机制' : ['能量机制：忍者使用能量而非法力，','故可以免疫中毒和沉默，其回复机制','与回蓝机制相同，但无法从回蓝效果','(如装备、海洋羁绊、技能等)中获益'],\
		'感电状态' : ['感电状态：处于感电状态的单位会吸','引由雷霆羁绊产生的落雷，并且需要','多承受50%落雷伤害'],\
		'压制状态' : ['压制状态：施法者在压制期间处于不','可阻挡状态且不会被沉默打断，优先','级高于强制施法、不可阻挡状态、水','银披风净化，低于无敌状态'],\
		'灼烧状态' : ['灼烧状态：除了造成真实伤害，灼烧','状态还可减少目标40%的生命值回复','灼烧状态受法强加成且会被冰冻状态','覆盖'],\
		'冰冻状态' : ['冰冻状态：几乎与眩晕状态一样，不','同的是冰冻状态会被灼烧状态覆盖'],\
		'重伤状态' : ['重伤状态：减少目标70%的生命值回','复'], \
		'减伤状态' : ['减伤状态：%d%%减伤' % int((1 - self.champion.condition.matigation.value)*100),'(不能减免真实伤害)'], \
		'低语补充说明' : ['低语补充说明：触发剑士羁绊时，低','语的额外攻速转AD收益下降，相当于','攻速只乘以2'], \
		'暗星能量' : ['暗星能量层数：%d' % self.champion.flag.rela_flag['暗星'][3],'提升伤害倍数：%d%%' % int(self.champion.flag.rela_flag['暗星'][3]*self.champion.flag.rela_flag['暗星'][1]*100)], \
		'破法状态' : ['破法状态：最大法力值提升40%，直','到施放一次技能后恢复，破法效果不','会叠加']}
		if version[0] == 3:
			description['灼烧状态'] = ['灼烧状态：每秒灼烧目标1.5%最大生','命值的真实伤害(受法强加成)，并减','少目标40%的生命值回复']
		if self.champion.position == 0:
			para_rect_x = self.base_x-167-49
			damage_rect_x = para_rect_x
		else:
			para_rect_x = self.base_x+267+5
			damage_rect_x = para_rect_x
		special_rect = para_rect_x, self.base_y[self.champion.pos_num]+155, 157+49, 70
		pygame.draw.rect(self.screen,gray,special_rect,0)
		font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 12)
		des_len = len(description[mechanism])
		for i in range(des_len):
			text = font.render(('%s' % description[mechanism][i]), 1, (0,0,0))
			self.screen.blit(text,(para_rect_x+8, self.base_y[self.champion.pos_num]+159+16*i))
	# 显示羁绊图标
	def Relatedness(self,pos_mouse):
		rela_color = {0 : gray, 1 : gray, 2 : white, 3 : orange_yellow, 4 : yellow}
		# 羁绊
		r_color = [gray,gray]
		r = [self.champion.champion.relatedness.element[1],self.champion.champion.relatedness.profession[1]]
		for i in range(2):
			r_color[i] = rela_color[r[i]]
		#	元素
		ele_c = self.base_x+20+8, self.base_y[self.champion.pos_num]+50+8
		pygame.draw.circle(self.screen,r_color[0],ele_c,8,0)
		ele = self.champion.champion.relatedness.element[0]
		e_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(ele)]-1][0]
		if self.champion.flag.rela_flag[ele][2][0]:
			if ele == '暗星':
				e_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(ele)]-1][1]
			else:
				show_rela_end_flag = self.rela_time_count[ele].Duration(self.champion.flag.rela_flag[ele][2][1])
				if show_rela_end_flag:
					self.champion.flag.rela_flag[ele][2][0] = False
				else:
					e_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(ele)]-1][1]
		self.screen.blit(e_pic,(self.base_x+20, self.base_y[self.champion.pos_num]+50))
		#	职业
		pro_c = self.base_x+20+8,self.base_y[self.champion.pos_num]+50+20+8
		pygame.draw.circle(self.screen,r_color[1],pro_c,8,0)
		pro = self.champion.champion.relatedness.profession[0]
		p_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(pro)]-1][0]
		if self.champion.flag.rela_flag[pro][2][0]:
			if pro in ('忍者','忍剑士'):
				p_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(pro)]-1][1]
			else:
				show_rela_end_flag = self.rela_time_count[pro].Duration(self.champion.flag.rela_flag[pro][2][1])
				if show_rela_end_flag:
					self.champion.flag.rela_flag[pro][2][0] = False
				else:
					p_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(pro)]-1][1]
		self.screen.blit(p_pic,(self.base_x+20, self.base_y[self.champion.pos_num]+50+20))
		#	额外
		if self.champion.champion.relatedness.extra[0] != 'None':
			ext_c = self.base_x+20+8,self.base_y[self.champion.pos_num]+50+40+8
			ext_color = rela_color[self.champion.champion.relatedness.extra[1]]
			pygame.draw.circle(self.screen,ext_color,ext_c,8,0)
			ext = self.champion.champion.relatedness.extra[0]
			ext_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(ext)]-1][0]
			if self.champion.flag.rela_flag[ext][2][0]:
				if ext in ('忍者','暗星'):
					ext_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(ext)]-1][1]
				else:
					show_rela_end_flag = self.rela_time_count[ext].Duration(self.champion.flag.rela_flag[ext][2][1])
					if show_rela_end_flag:
						self.champion.flag.rela_flag[ext][2][0] = False
					else:
						ext_pic = self.rela_pic[list(r_dic.keys())[list(r_dic.values()).index(ext)]-1][1]
			self.screen.blit(ext_pic,(self.base_x+20, self.base_y[self.champion.pos_num]+50+40))
		# 羁绊效果显示
		rela_rect = self.base_x, self.base_y[self.champion.pos_num]+155, 249, 70
		d = [1000 for _ in range(3)]
		d[0] = ((pos_mouse[0]-(self.base_x+28))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+58))**2)
		d[1] = ((pos_mouse[0]-(self.base_x+28))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+78))**2)
		if self.champion.champion.relatedness.extra[0] != 'None':
			d[2] = ((pos_mouse[0]-(self.base_x+28))**2 + (pos_mouse[1]-(self.base_y[self.champion.pos_num]+98))**2)
		if d[0] <= 64 or d[1] <= 64 or d[2] <= 64:
			pygame.draw.rect(self.screen,gray,rela_rect,0)
			rfont = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 14)
			if d[0] <= 64:
				des_len = len(rela_dic[self.champion.champion.relatedness.element[0]][0])
				e_color = [black, white, white, white]
				for i in range(des_len):
					if self.champion.champion.relatedness.element[0] in ('黯焰','银河魔装机神','异星人'):
						e_color[i] = black
					elif self.game.LR_rela[self.champion.position][self.champion.champion.relatedness.element[0]] == i+1:
						e_color[i] = black
					if self.champion.champion.relatedness.element[0] in ('银月','剧毒','星之守护者','奥德赛','源计划','星神','暗星','银河机神') and i > 0:
						j = i - 1
					else:
						j = i
					e_text = rfont.render(("%s" % rela_dic[self.champion.champion.relatedness.element[0]][0][i]), 1, e_color[j])
					self.screen.blit(e_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
			elif d[1] <= 64:
				des_len = len(rela_dic[self.champion.champion.relatedness.profession[0]][0])
				p_color = [black, white, white, black]
				for i in range(des_len):
					if self.champion.champion.relatedness.profession[0] in ('大元素使','恕瑞玛之皇','太阳圆盘','星舰龙神'):
						p_color[i] = black
					elif self.game.LR_rela[self.champion.position][self.champion.champion.relatedness.profession[0]] == i+1:
						p_color[i] = black
					if self.champion.champion.relatedness.profession[0] in ('狂战士','枪手','剑士','忍者','爆破专家','法师','刺客') and i > 0:
						j = i - 1
					else:
						j = i
					p_text = rfont.render(("%s" % rela_dic[self.champion.champion.relatedness.profession[0]][0][i]), 1, p_color[j])
					self.screen.blit(p_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
			elif d[2] <= 64 and self.champion.champion.relatedness.extra[0] != 'None':
				des_len = len(rela_dic[self.champion.champion.relatedness.extra[0]][0])
				ext_color = [black, white, white, white]
				for i in range(des_len):
					if self.game.LR_rela[self.champion.position][self.champion.champion.relatedness.extra[0]] == i+1:
						ext_color[i] = black
					if self.champion.champion.relatedness.extra[0] in ('狂战士','剑士','忍者','爆破专家','星之守护者','奥德赛','星神','暗星','法师','刺客') and i > 0:
						j = i - 1
					else:
						j = i
					ext_text = rfont.render(("%s" % rela_dic[self.champion.champion.relatedness.extra[0]][0][i]), 1, ext_color[j])
					self.screen.blit(ext_text,(self.base_x+8, self.base_y[self.champion.pos_num]+159+16*i))
		# 特殊机制介绍
		#	能量机制介绍
		if (d[1] <= 64 and self.champion.champion.relatedness.profession[0] in ('忍者','忍剑士')) \
		or (d[2] <= 64 and self.champion.champion.relatedness.extra[0] == '忍者'):
			self.Special_mechanism_description('能量机制')
		elif ((d[0] <= 64 and self.champion.champion.relatedness.element[0] == '极地') \
		or (d[2] <= 64 and self.champion.champion.relatedness.extra[0] == '极地')) and version[0] == 1:
			self.Special_mechanism_description('冰冻状态')
		elif (d[0] <= 64 and self.champion.champion.relatedness.element[0] in ('地狱火','黯焰')) \
		or (d[2] <= 64 and self.champion.champion.relatedness.extra[0] == '地狱火'):
			self.Special_mechanism_description('灼烧状态')
		elif (d[1] <= 64 and self.champion.champion.relatedness.profession[0] == '恕瑞玛之皇'):
			self.Special_mechanism_description('减伤状态')
		elif (d[0] <= 64 and self.champion.champion.relatedness.element[0] == '异星人'):
			self.Special_mechanism_description('减伤状态')
		elif d[2] <= 64 and self.champion.champion.relatedness.extra[0] == '剑士' and self.champion.champion.name == 'Jhin':
			self.Special_mechanism_description('低语补充说明')
		elif ((d[0] <= 64 and self.champion.champion.relatedness.element[0] == '暗星') \
		or (d[2] <= 64 and self.champion.champion.relatedness.extra[0] == '暗星')) and self.champion.flag.rela_flag['暗星'][0]:
			self.Special_mechanism_description('暗星能量')
	# 显示效果指示灯：依次是祈愿、冲击之潮、烈焰风暴、曲光屏障、狂热电刀、离子火花、卢登回声、冰脉护手、光之祭献、魂引之灯、羊灵生息、沙兵攻击、安魂曲
	# 魔偶攻击、冰风暴、月光、净化剑刃、活体大炮、来自艾卡西亚的惊喜、落雷、荧焰、飞轮、月之驻灵、天雷、提伯斯攻击、欺诈宝珠、金色卡牌、红色卡牌、蓝色卡牌
	# 时间、皮克斯攻击、鼓舞、陨星、轰炸、鱼骨头、圆盾、炮台攻击、古灵精怪、死亡祭献、闪电链
	def Effect(self):
		for i in range(4):
			effect_bg_c = self.base_x+8, self.base_y[self.champion.pos_num]+32+21*i
			pygame.draw.circle(self.screen,gray,effect_bg_c,5,0)	
		effect1 = [['祈愿',light_green3],['冲击之潮',gray_blue],['烈焰风暴',orange_red],['曲光屏障',white],['狂热电刀',orange_yellow],\
		['离子火花',blue2],['卢登回声',purple],['冰脉护手',dark_blue],['光之祭献',yellow],['魂引之灯',dark_green],['羊灵生息',light_green],\
		['沙兵攻击',gray_orange],['安魂曲',dark_cyan],['魔偶攻击',gray_blue2],['月光',silver],['净化剑刃',yellow],['活体大炮',yellow_green],\
		['来自艾卡西亚的惊喜',dark_purple],['落雷',blue],['荧焰',bule_purple],['飞轮',gary_green],['月之驻灵',white_green],['天雷',light_yellow2],\
		['提伯斯攻击',orange_red],['欺诈宝珠',pink],['金色卡牌',yellow],['红色卡牌',red],['蓝色卡牌',blue],['时间',(194, 255, 255)],['皮克斯攻击',white_green],\
		['陨星',(107, 78, 203)],['轰炸',orange],['鱼骨头',(136, 143, 217)],['圆盾',white],['炮台攻击',black],['古灵精怪',gray_blue],\
		['死亡祭献',dark_purple],['闪电链',(71, 80, 164)]]
		effect2 = [['冰风暴',light_blue],['鼓舞',(27, 155, 102)]]
		effect_number = 0
		for i in range(len(effect1)):
			if self.champion.flag.special_flag.effect[effect1[i][0]][0]:
				effect_show_end_flag = self.effect_time_count[effect1[i][0]].Duration(self.champion.flag.special_flag.effect[effect1[i][0]][1])
				if effect_show_end_flag:
					self.champion.flag.special_flag.effect[effect1[i][0]][0] = False
				else:
					effect_c = self.base_x+8, self.base_y[self.champion.pos_num]+32+21*effect_number
					pygame.draw.circle(self.screen,effect1[i][1],effect_c,5,0)
					effect_number += 1
		for i in range(len(effect2)):
			if self.champion.flag.special_flag.effect[effect2[i][0]][0]:
				effect_c = self.base_x+8, self.base_y[self.champion.pos_num]+32+21*effect_number
				pygame.draw.circle(self.screen,effect2[i][1],effect_c,5,0)
				effect_number += 1
	# 显示光环指示灯：依次是冰霜之心、基克先驱、深渊面具
	def Halo(self):
		for i in range(3):
			halo_bg_c = self.base_x+241, self.base_y[self.champion.pos_num]+53+21*i
			pygame.draw.circle(self.screen,gray,halo_bg_c,5,0)
		halo = [['冰霜之心',white_blue],['基克先驱',light_red],['深渊面具',dark_pink]]	
		halo_number = 0
		for i in range(3):
			if self.champion.flag.special_flag.halo[halo[i][0]]:
				halo_c = self.base_x+241, self.base_y[self.champion.pos_num]+53+21*halo_number
				pygame.draw.circle(self.screen,halo[i][1],halo_c,5,0)
				halo_number += 1
	# 绘制沙兵or月之驻灵or炮台
	def Draw_sand_battery(self):
		for i in range(3):
			Dsd = [sand[i],moonbattery[i],battery[i]]
			if Dsd[version[0] - 1].flag:
				# 图标
				if version[0] == 1:
					pic = pygame.image.load('pic/Champion/Azir/沙兵%d.png' % sand[i].position)
				elif version[0] == 2:
					pic = pygame.image.load('pic/Champion/Aphelios/月之驻灵%d.png' % Dsd[version[0] - 1].position)
				elif version[0] == 3:
					if not Dsd[version[0] - 1].super_flag:
						pic = pygame.image.load('pic/Champion/Heimerdinger/H-28G进化炮台%d.png' % Dsd[version[0] - 1].position)
					else:
						pic = pygame.image.load('pic/Champion/Heimerdinger/H-28Q尖端炮台%d.png' % Dsd[version[0] - 1].position)
				if Dsd[version[0] - 1].position == 0:
					x = 675 + 343
				else:
					x = 277 - 148
				self.screen.blit(pic,(x, self.base_y[Dsd[version[0] - 1].pos_num]+55))
	# 绘制伙伴：魔偶/皮克斯
	def Draw_partner(self,mode):
		if mode == 0:
			golem_pic = pygame.image.load('pic/Champion/Orianna/魔偶.png')
			self.screen.blit(golem_pic,(golem.current_point[0],golem.current_point[1]))
		elif mode == 1:
			pix_pic = pygame.image.load('pic/Champion/Lulu/皮克斯.png')
			self.screen.blit(pix_pic,(pix.current_point[0],pix.current_point[1]))
	# 绘制提伯斯
	def Tibbers(self):
		# 提伯斯
		pic = pygame.image.load('pic/Champion/Annie/提伯斯%d.png' % tibbers.position)
		self.screen.blit(pic,(580,(self.base_y[tibbers.pos_num]+55)))
		# 提伯斯的血条
		# 血条背景
		hp_bg_rect = 580, self.base_y[tibbers.pos_num]+100, 40, 5
		pygame.draw.rect(self.screen,black,hp_bg_rect,0)
		# 血条
		if tibbers.shield_value > 0:
			if tibbers.hp_value + tibbers.shield_value > tibbers.hp_max_value:
				shield_width = 40
				hp_width = int(40 * (tibbers.hp_value / (tibbers.hp_max_value + tibbers.shield_value)))
			else:
				shield_width = int(40*((tibbers.hp_value + tibbers.shield_value) / tibbers.hp_max_value))
				hp_width = int(40 * (tibbers.hp_value / tibbers.hp_max_value))
			shield_rect = 580, self.base_y[tibbers.pos_num]+100, shield_width, 5
			pygame.draw.rect(self.screen,white,shield_rect,0)
		else:
			hp_width = int(40 * (tibbers.hp_value / tibbers.hp_max_value))
		hp_rect = 580, self.base_y[tibbers.pos_num]+100, hp_width, 5
		color_hp = red
		pygame.draw.rect(self.screen,color_hp,hp_rect,0)
	# 绘制战斗机
	def Draw_warcraft(self,mode):
		for num in range(6):
			if mode == 0 and not warcraft[num].flag:
				warcraft_pic = pygame.image.load('pic/Champion/AurelionSol/战斗机%d.png' % warcraft[num].direction)
				self.screen.blit(warcraft_pic,(warcraft[num].current_point[0],warcraft[num].current_point[1]))
			elif mode == 1 and warcraft[num].flag:
				warcraft_pic = pygame.image.load('pic/Champion/AurelionSol/战斗机%d.png' % warcraft[num].direction)
				self.screen.blit(warcraft_pic,(warcraft[num].current_point[0],warcraft[num].current_point[1]))
	# 绘制枪手额外攻击的弹道
	def Trajectory(self):
		# 起始点坐标
		x = [542,659]
		y = [125,355,585]
		if self.champion.flag.rela_flag['枪手'][0]:
			for i in range(2):
				if self.champion.flag.rela_flag['枪手'][5][i] != None:
					pygame.draw.aaline(self.screen, orange_red, (x[self.champion.position], y[self.champion.pos_num]), \
						(x[~self.champion.position+2], y[self.champion.flag.rela_flag['枪手'][5][i]]), 1)
					end_flag = self.clean_count[0][i].Duration(self.clean_count[1])
					if end_flag:
						self.champion.flag.rela_flag['枪手'][5][i] = None
	# 绘制炮台的镭射光线
	def Laser(self):
		for i in range(3):
			if battery[i].flag and battery[i].laser[0]:
				# 起点坐标
				sx = [1013,174]
				sy = [125,355,585]
				# 终点坐标
				dx = [272,929]
				dy = [125,355,585]
				if battery[i].laser[0]:
					pygame.draw.aaline(self.screen, light_blue, (sx[battery[i].position], sy[battery[i].pos_num]), \
						(dx[battery[i].laser[1].position], dy[battery[i].laser[1].pos_num]), 1)
					if self.clean_count2[i][0].Duration(self.clean_count2[i][1]):
						battery[i].laser[0] = False
	# 亚索亮牌
	def Happy(self):
		if self.champion.champion.skill.para[4][0]:
			# 图片
			pic = pygame.image.load('pic/Champion/Yasuo/牌子/%d.png' % (self.champion.champion.skill.para[4][1]))
			if self.champion.position == 0:
				x = self.base_x-70-76
			else:
				x = self.base_x+249+70
			self.screen.blit(pic,(x, self.base_y[self.champion.pos_num]+75-35))
			end_flag = self.champion.champion.skill.para[4][2].Duration(self.champion.champion.skill.para[4][3])
			if end_flag:
				self.champion.champion.skill.para[4][1] += 1
				if self.champion.champion.skill.para[4][1] == 41:
					self.champion.champion.skill.para[4][1] = 1
					self.champion.champion.skill.para[4][0] = False
	# 兰博火焰
	def Fire(self):
		if self.champion.champion.skill.para[5][0]:
			# 图片
			pic = pygame.image.load('pic/Champion/Rumble/fire%d/fire%d%d.png' % (self.champion.position,self.champion.position,self.champion.champion.skill.para[5][1]))
			if self.champion.position == 0:
				x = self.base_x+249
			else:
				x = self.base_x-119
			self.screen.blit(pic,(x, self.base_y[self.champion.pos_num]+75-122))
			end_flag = self.champion.champion.skill.para[5][2].Duration(self.champion.champion.skill.para[5][3])
			if end_flag:
				self.champion.champion.skill.para[5][1] += 1
				if self.champion.champion.skill.para[5][1] == 27:
					self.champion.champion.skill.para[5][1] = 0
					self.champion.champion.skill.para[5][0] = False
	# 波比屏障
	def Obstacle(self,champion):
		x = 530 + champion.position * 137
		if champion.pos_num == 0:
			y = self.base_y[0]-4
			l = 388
		elif champion.pos_num == 1:
			y = self.base_y[champion.pos_num - 1]-4
			l = 618
		else:
			y = self.base_y[champion.pos_num - 1]-4
			l = 388
		rect = x, y, 4, l
		pygame.draw.rect(self.screen,yellow,rect,0)
	# 更新图
	def Draw(self,pos_mouse):
		if sky_color[0] == white:
			text_color = black
		else:
			text_color = white
		font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 16)
		# 显示回合数
		Round_rect = 560,45,80,30
		pygame.draw.rect(self.screen,gray,Round_rect,0)
		time_text = font.render(('Round:%d' % Round[0]), 1, black)
		if Round[0] < 10:
			self.screen.blit(time_text,(572,52))
		else:
			self.screen.blit(time_text,(570,52))
		# 显示游戏时间
		time_rect = 560,80,80,30
		pygame.draw.rect(self.screen,gray,time_rect,0)
		time_text = font.render(('%d' % self.game.time), 1, black)
		if self.game.time < 10:
			self.screen.blit(time_text,(594,87))
		else:
			self.screen.blit(time_text,(592,87))
		# 显示左右分值栏
		point_rect = [(371,10,61,30),(769,10,61,30)]
		pygame.draw.rect(self.screen,gray,point_rect[0],0)
		point_text_l = font.render('%d' % point[0], 1, black)
		if point[0] > 9:
			self.screen.blit(point_text_l,(394,16))
		else:
			self.screen.blit(point_text_l,(396,16))
		pygame.draw.rect(self.screen,gray,point_rect[1],0)
		point_text_l = font.render('%d' % point[1], 1, black)
		if point[1] > 9:
			self.screen.blit(point_text_l,(394+397,16))
		else:
			self.screen.blit(point_text_l,(396+397,16))
		if self.game.obstacle_flag[0] and self.champion.pos_num == 0 and self.champion.position == 0:
			self.Obstacle(self.game.obstacle_flag[1])
		self.Bg()
		self.Name()
		self.Action()
		self.Hpmp()
		if self.champion.champion.name == 'Aphelios':
			self.Chakram(self.champion)
		if self.game.warcraft_flag and self.champion.champion.name == 'AurelionSol':
			self.Draw_warcraft(0)
		self.Weapon(pos_mouse)
		self.Condition()
		self.Enemy()
		self.Skill(pos_mouse)
		self.Para(pos_mouse)
		self.Relatedness(pos_mouse)
		self.Effect()
		self.Halo()
		self.Draw_sand_battery()
		if golem.flag:
			self.Draw_partner(0)
		elif pix.flag:
			self.Draw_partner(1)
		self.Trajectory()
		if self.champion.champion.name == 'Yasuo' and version[0] == 2:
			self.Happy()
		elif self.champion.champion.name == 'Rumble':
			self.Fire()
		elif self.champion.champion.name == 'Heimerdinger':
			self.Laser()
		if tibbers.flag:
			self.Tibbers()
		if self.game.warcraft_flag:
			self.Draw_warcraft(1)
		# 重新开始(按钮)
		restart_rect = 560, 10, 80, 30
		pygame.draw.rect(self.screen,gray,restart_rect,0)
		restart_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 20)
		restart_text = restart_font.render("RESTART", 1, black)
		self.screen.blit(restart_text,(565, 14))
		# 显示海牛加时赛
		if self.game.urf[0] > 0:
			urf_text = font.render(('Urf！× %d' % self.game.urf[0]), 1, text_color)
			self.screen.blit(urf_text,(565, 125))

def main():
	# BGM
	bgm = r'bgm.mp3'
	# 处理pygame
	pygame.init()
	pygame.mixer.init()
	# 加载音乐文件
	pygame.mixer.music.load(bgm)
	# 播放bgm
	pygame.mixer.music.play()
	# 标题
	logo = pygame.image.load('pic/lol.ico')
	pygame.display.set_icon(logo)
	pygame.display.set_caption('瓦洛兰战役')    												# 初始化pygame
	# 设置画布
	size = width, height = 1200, 850  								# 设置窗口大小
	screen = pygame.display.set_mode(size)							# 显示窗口
	# 创建左右方英雄
	if version[0] == 1:
		cp_number = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
	elif version[0] == 2:
		cp_number = [2,22,23,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
	elif version[0] == 3:
		cp_number = [8,15,42,44,45,49,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73]
	restart_flag = False
	while True:
		screen.fill(white)
		shuffle(cp_number)
		#cp_number = [50,47,39, 44,45,42]
		pos_mouse = [0,0]
		game = Game(cp_number,screen)
		text_content = ''
		restart_flag = False
		Round[0] += 1
		while True:
			if restart_flag:
				sleep(2)
				break
			while True:
				pygame.init() 
				for event in pygame.event.get():   # 遍历所有事件
					if event.type == pygame.QUIT:   # 如果单击关闭窗口，则退出
						sys.exit()
					elif event.type == MOUSEMOTION:
						pos_mouse = pygame.mouse.get_pos()
					elif event.type == MOUSEBUTTONDOWN and (560<=pos_mouse[0]<=640 and 10<=pos_mouse[1]<=40):
						restart_flag = True
					elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
						restart_flag = True
				if restart_flag:
					break
				for i in range(3):
					for j in range(2):
						game.LR[j][i].Attack()
				# 处理娜美的水潮
				if tide.flag:
					tide.Flow()
				# 处理布兰德的火球
				if fireball.flag:
					fireball.Jump()
				# 处理拉克丝的魔杖
				if wand.flag:
					wand.Fly()
				# 处理太阳圆盘召唤仪式(持续2s)
				if game.SolarDisk[0]:
					game.Tyyp(game.SolarDisk[3],game.SolarDisk[4])
				text_content = game.Finish_judg()
				# 处理奥莉安娜的魔偶
				if golem.flag:
					golem.Move()
				# 皮克斯
				if pix.flag:
					pix.Move()
				# 提伯斯
				if tibbers.flag:
					tibbers.Attack()
				# 月之驻灵
				for i in range(3):
					if moonbattery[i].flag:
						moonbattery[i].Attack()
				# 炮台
				for i in range(3):
					if battery[i].flag:
						battery[i].Attack()
				# 战斗机
				for num in range(6):
					if warcraft[num].flag:
						warcraft[num].Fly()
				# 机神合体
				for i in range(2):
					if game.MechWarrior_flag[i][0] and not game.MechWarrior_flag[i][3][0]:
						game.MechWarrior_Link(i)
				if text_content != 'Continue':
					# 计算分值
					for i in range(2):
						for j in range(3):
							if not game.LR[i][j].flag.condition_flag.death_flag:
								point[~i+2] -= 1
								if point[~i+2] <= 0:
									point[~i+2] = 0
					if point[0] == 0 or point[1] == 0:
						restart_flag = False
						break
					else:
						restart_flag = True
				sleep(0.01)
				Sky(screen,False)
				# 判断海牛加时赛
				game.Urf(screen)
				game.Show_ui(pos_mouse)
				pygame.display.update()
			Sky(screen,True)
			game.Show_ui(pos_mouse)
			if text_content != 'Continue':
				text_font = pygame.font.Font("C:/Temp/BOV/simhei.ttf", 19)
				text = text_font.render(('%s' % text_content), 1, white)
				screen.blit(text,(575, 155))
			pygame.display.update()

	pygame.quit()

if __name__ == '__main__':
	main()