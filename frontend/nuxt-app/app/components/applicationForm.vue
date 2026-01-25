<template>
    <Vueform size="md" :endpoint="false" validate-on="step" :float-placeholders="false" add-class="vf-application-form"
        ref="form$" @change="updateData" :onSubmit="handleSubmit">
        <template #empty>
            <FormSteps>
                <FormStep name="page0" :elements="[
                    'register_title',
                    'h2_4',
                    'p_7',
                    'h3_7',
                    'h3_13',
                    'p_13',
                    'p_2',
                    'h3_8',
                    'p_6',
                    'h3_10',
                    'p_8',
                    'h3_12',
                    'p_9',
                    'divider',
                    'checkbox',
                ]" label="开始" />
                <FormStep name="page1" :elements="[
                    'h2',
                    'h3',
                    'name',
                    'wxid',
                    'sex',
                    'school',
                    'email',
                    'grade',
                    'timezone',
                    'location',
                    'divider_1',
                    'h3_1',
                    'p',
                    'mbti_ei',
                    'mbti_sn',
                    'mbti_tf',
                    'mbti_jp',
                    'divider_2',
                ]" label="关于你" />
                <FormStep name="page2" :elements="[
                    'h2_1',
                    'hobbies',
                    'travel_destination',
                    'superpower',
                    'use_of_money',
                    'family',
                    'lifestyle',
                    'divider_3',
                ]" label="更多" />
                <FormStep name="page3" label="关于ta" :elements="[
                    'h2_2',
                    'h3_2',
                    'p_1',
                    'preferred_sex',
                    'preferred_grades',
                    'preferred_schools',
                    'max_time_difference',
                    'same_location_only',
                    'divider_4',
                    'h3_3',
                    'p_3',
                    'radioTabs',
                    'preferred_mbti_ei',
                    'preferred_mbti_sn',
                    'preferred_mbti_tf',
                    'preferred_mbti_jp',
                    'divider_6',
                    'h3_4',
                    'preferred_wxid',
                    'continue_match',
                    'divider_5',
                ]" />
                <FormStep name="page4" label="结束" :elements="[
                    'h2_3',
                    'h3_11',
                    'message_to_partner',
                    'divider_7',
                    'h3_6',
                    'comment',
                    'confirm1',
                    'confirm2',
                    'divider_8',
                ]" />
            </FormSteps>

            <FormElements>
                <StaticElement name="register_title" tag="h1" content="Triple Uni 一周CP 2026 活动报名问卷" />
                <StaticElement name="h2_4" tag="h2" content="活动须知  (请全部阅读)" top="1" />
                <StaticElement name="h3_9" tag="h3" content="形式" top="1" />
                <StaticElement name="p_7" tag="p" content="
            <div>
                <strong>本次活动为自助形式, 参与者需要访问本网址 (https://valentine.tripleuni.com)&nbsp; 获取匹配结果, 支付押金, 查看与提交每日任务等...</strong><br>
                <br>
                匹配成功的小组会被分配一位Mentor, ta的联系方式将在本网站展示, 请参与者主动添加Mentor并备注对应的编号, 在活动过程中如有疑问或遇到问题都可以与你们的Mentor联系.
            </div>" />

                <StaticElement name="h3_7" tag="h3" content="时间线(北京时间)" top="2" />
                <StaticElement name="p_2" tag="p" content="
            <div>
                <ol>
                    <li class='vf-li'>2月1日06:00 AM - 开始报名</li>
                    <li class='vf-li'>2月5日23:59 PM - 报名截止</li>
                    <li class='vf-li'>2月6日06:00 AM - 公布第一轮匹配结果</li>
                    <li class='vf-li'><strong>2月7日06:00 AM- 第一轮确认截止</strong></li>
                    <li class='vf-li'>2月7日12:00 PM - 公布第二轮匹配结果</li>
                    <li class='vf-li'>2月7日22:00 PM - 双方可查看对方微信号并自主添加</li>
                    <li class='vf-li'>2月8日00:00 AM - 第一天任务公布, 活动正式开始</li>
                    <li class='vf-li'>2月9日00:00 AM - 第二天任务公布</li>
                    <li class='vf-li'>2月9日05:59 AM - 第一天任务提交截止</li>
                    <div style='width: 100%; line-height: 1; height: 1.5em; text-align: center;scale: 1.25;'>
                    ...
                    </div>
                    <li class='vf-li'>2月15日05:59 AM - 第七天任务提交截止</li>
                    <li class='vf-li'>2月16日23:59 - 反馈问卷提交截止</li>
                </ol>
            </div>" />
                <StaticElement name="h3_13" tag="h3" content="关于匹配" top="2" />
                <StaticElement name="p_13" tag="p" content="
            <div>
               本次活动共分为两轮匹配:
               <ul>
                <li class='vf-li'>
                    第一轮匹配:<br>
                    系统将会根据你的个人信息和偏好进行匹配, 若匹配成功, 你需要在<strong>第一轮确认截止前选择是否接受此CP组.</strong> 若双方均接受, 则组队成功. 若有一方或双方未做出选择或拒绝匹配, 则此轮组队失败. <br>
                    所有在第一轮未被匹配以及第一轮组队失败的申请人将会参与第二轮匹配. 未对匹配结果做出选择的申请人将在第二轮匹配中被<strong>降低权重</strong>.
                </li>
                <br>
                <li class='vf-li'>
                    第二轮匹配: <br>
                    此为最终轮次匹配, <strong>不论你是否被第一轮匹配选中</strong>, 匹配成功即视为组队成功, 你<strong>无法</strong>要求重新匹配或退出活动.<br>
                    在第二轮中依旧没有被匹配的申请人将会被视为匹配失败, 我们会退还你的全部押金.
                </li>
               </ul>
               <br>
                在报名截止后匹配结束前,若因特殊情况需要退出活动, 请及时联系主办方, 我们将视情况为你做出安排.
            </div>" />
                <StaticElement name="h3_8" tag="h3" content="关于押金" top="2" />
                <StaticElement name="p_6" tag="p" content="
            <div>
                为了对所有参与者负责, 我们为此次活动设置了<strong>99元押金</strong>(人民币).<br>
                <br>
                押金构成如下:<br>
                <ul>
                    <li class='vf-li'>70元: 完成每日基础任务 (10元/天)</li>
                    <li class='vf-li'>20元: 完成活动</li>
                    <li class='vf-li'>9元: 完成反馈问卷</li>
                </ul>
                <strong>若完成的基础任务不足3天, 则所有押金将不予退还</strong><br>
                <br>
                押金将在报名时收取, <strong>只有成功缴纳才视为报名完成.</strong><br>
                在报名截止前, 你可以随时选择退出活动并获得全额退款.报名截止后, 你必须完成所有基础活动内容方可获得押金退还.<br>
                <br>
                如果因为对方原因导致无法继续活动, 请及时联系你的Mentor并说明情况, 我们将会视情况为你做出安排<br>
                <br>
                押金将在活动结束后30日内原路退还.<br>

                

            </div>" />
                <StaticElement name="h3_10" tag="h3" content="数据收集 & 隐私承诺" top="2" />
                <StaticElement name="p_8" tag="p" content="
            <div>
                我们将会收集并保存以下隐私信息:<br>
                <br>
                [通过微信登陆授权]<br>
                <ul>
                    <li class='vf-li'>你的微信头像</li>
                    <li class='vf-li'>你的微信昵称</li>
                    <li class='vf-li'>你的微信OpenID (用作网站登陆, 微信支付)</li>
                </ul>
                <br>
                [通过填写问卷]<br>
                <ul>
                    <li class='vf-li'>所有在问卷中填写的所有内容</li>
                </ul>
                <br>
                [参与活动]<br>
                <ul>
                    <li class='vf-li'>你提交的所有任务内容</li>
                    <li class='vf-li'>你提交的反馈问卷</li>
                </ul>
                <br>
                我们承诺将尽最大努力妥善保管你的隐私数据, 秉承最小权限原则限制他人不必要的访问.&nbsp;<br>
                我们承诺不会将这些数据提供给无关第三方.<br>
                <br>
                <strong>你的任务将由人工智能模型自动评分, 在没有你的允许下Mentor无法看到你提交的内容. 为了确保能够准确评分, 请不要遮挡/ 修改/ 模糊你提交的任务.</strong><br>
            </div>" />
                <StaticElement name="h3_12" tag="h3" content="故障自助处理" top="2" />
                <StaticElement name="p_9" tag="p"
                    content="<div>如果你在网站上遇到了错误, 可以尝试以下步骤修复:<br><br> 1. 打开网站首页<br> 2. 点击左上方的「?」 标签<br> 3. 点击「清除页面缓存」按钮<br> 4. 重新登录</div>" />
                <StaticElement name="divider" tag="hr" top="2" />
                <CheckboxElement name="checkbox" field-name="规则及隐私条款" :rules="['accepted']"
                    text="我已详细阅读、理解并同意以上所有内容并愿意参加活动。" :submit="false" />

                <StaticElement name="h2" tag="h2" content="个人信息" />
                <StaticElement name="h3" tag="h3" content="基础信息" />
                <TextElement name="name" field-name="姓名" label="你的中文全名" placeholder="张三"
                    :rules="['required', 'max:4']" />
                <TextElement name="wxid" field-name="微信号" :columns="{
                    label: 12,
                    wrapper: 12,
                }" :rules="['required', 'max:50']" label="你的微信号"
                    description="请确定wxid正确，且可被搜索/ 添加。如果你的微信号是以wxid开头的原始id，请填入手机号。" placeholder="my_wechat_id" />
                <RadiogroupElement name="sex" field-name="性别" view="tabs" :items="[
                    {
                        value: 'M',
                        label: '男',
                    },
                    {
                        value: 'F',
                        label: '女',
                    },
                ]" label="你的性别" :rules="['required']" />
                <RadiogroupElement name="school" field-name="就读学校" view="blocks" :items="[
                    {
                        value: 'HKU',
                        label: 'HKU',
                        description: '',
                    },
                    {
                        value: 'CUHK',
                        label: 'CUHK',
                        description: '',
                    },
                    {
                        value: 'UST',
                        label: 'HKUST',
                        description: null,
                    },
                ]" label="你就读的学校" :rules="['required']" />
                <TextElement name="email" input-type="email" :rules="[
                    'regex:^[a-zA-Z0-9._%+-]+@(connect\\.ust\\.hk|connect\\.hku\\.hk|link\\.cuhk\\.edu\\.hk)$',
                    'email',
                    'required'
                ]" label="你的学校邮箱" placeholder="email@example.com" description="我们会发送验证码至此邮箱以验证归属, 请确认邮箱填写正确" />
                <RadiogroupElement name="grade" field-name="年级" view="blocks" :items="[
                    {
                        value: 'UG1',
                        label: '本科大一',
                        description: null,
                    },
                    {
                        value: 'UG2',
                        label: '本科大二',
                        description: null,
                    },
                    {
                        value: 'UG3',
                        label: '本科大三',
                        description: null,
                    },
                    {
                        value: 'UG4',
                        label: '本科大四',
                        description: null,
                    },
                    {
                        value: 'UG5',
                        label: '本科大五',
                        description: null,
                    },
                    {
                        value: 'MS',
                        label: '硕士生',
                        description: null,
                    },
                    {
                        value: 'PHD',
                        label: '博士生',
                        description: null,
                    },
                    {
                        value: 'PROF',
                        label: '教授',
                        description: null,
                    },
                ]" label="你目前的年级" :rules="['required']" />
                <SelectElement name="timezone" field-name="时区" :native="false" :items="[
                    { value: 'UTC-12', label: 'UTC-12:00 (贝克岛)' },
                    { value: 'UTC-11', label: 'UTC-11:00 (美属萨摩亚)' },
                    { value: 'UTC-10', label: 'UTC-10:00 (夏威夷)' },
                    { value: 'UTC-9', label: 'UTC-09:00 (阿拉斯加)' },
                    { value: 'UTC-8', label: 'UTC-08:00 (太平洋时间, 洛杉矶、温哥华)' },
                    { value: 'UTC-7', label: 'UTC-07:00 (山地时间, 丹佛、凤凰城)' },
                    { value: 'UTC-6', label: 'UTC-06:00 (中部时间, 芝加哥、墨西哥城)' },
                    { value: 'UTC-5', label: 'UTC-05:00 (东部时间, 纽约、多伦多)' },
                    { value: 'UTC-4', label: 'UTC-04:00 (大西洋时间, 哈利法克斯、圣地亚哥)' },
                    { value: 'UTC-3', label: 'UTC-03:00 (巴西、阿根廷)' },
                    { value: 'UTC-2', label: 'UTC-02:00 (南乔治亚)' },
                    { value: 'UTC-1', label: 'UTC-01:00 (亚速尔群岛)' },
                    { value: 'UTC+0', label: 'UTC+00:00 (伦敦、都柏林)' },
                    { value: 'UTC+1', label: 'UTC+01:00 (柏林、巴黎)' },
                    { value: 'UTC+2', label: 'UTC+02:00 (开罗、雅典)' },
                    { value: 'UTC+3', label: 'UTC+03:00 (莫斯科、迪拜)' },
                    { value: 'UTC+4', label: 'UTC+04:00 (阿布扎比)' },
                    { value: 'UTC+5', label: 'UTC+05:00 (巴基斯坦)' },
                    { value: 'UTC+5.5', label: 'UTC+05:30 (印度)' },
                    { value: 'UTC+6', label: 'UTC+06:00 (孟加拉国)' },
                    { value: 'UTC+7', label: 'UTC+07:00 (曼谷、雅加达)' },
                    { value: 'UTC+8', label: 'UTC+08:00 (北京、香港、新加坡)' },
                    { value: 'UTC+9', label: 'UTC+09:00 (东京、首尔)' },
                    { value: 'UTC+10', label: 'UTC+10:00 (悉尼、墨尔本)' },
                    { value: 'UTC+11', label: 'UTC+11:00 (所罗门群岛)' },
                    { value: 'UTC+12', label: 'UTC+12:00 (奥克兰、惠灵顿)' },
                ]" label="你所在的时区" placeholder="选择你的时区" :default="defaultTimezone" :rules="['required']" />
                <SelectElement name="location" field-name="所在地区" :native="false" :items="[
                    { value: 'HK', label: '香港' },
                    { value: 'SZ', label: '深圳' },
                    { value: 'GD', label: '广东省' },
                    { value: 'TW', label: '台湾' },
                    { value: 'CN', label: '中国' },
                    { value: 'JP_KR', label: '日韩' },
                    { value: 'ASIA', label: '亚洲' },
                    { value: 'UK', label: '英国' },
                    { value: 'EU', label: '欧洲' },
                    { value: 'US', label: '美国' },
                    { value: 'CA', label: '加拿大' },
                    { value: 'NA', label: '北美洲' },
                    { value: 'OTHER', label: '其他' },
                ]" label="你本学期最常在的地区" :rules="['required']" description="请选择最精确(小)的选项。如果你在多个地区之间频繁往返，请选择你待的时间最长的地区。" />
                <StaticElement name="divider_1" tag="hr" top="1" bottom="1" />
                <StaticElement name="h3_1" tag="h3" content="MBTI 性格测试结果" />
                <StaticElement name="p" tag="p"
                    content="<div>请通过滑动的方式选择你的MBTI.<br><br>如果你不确定自己的MBTI, 可以通过 <a href='https://www.16personalities.com\' target='blank'>https://www.16personalities.com (免费)</a><br>或其他网站进行测试.<br><br>别害怕! 你可以做完整个测试后再回来继续填写, <strong>所有进度将会被自动保存.</strong><br><br>如果你只知道自己的MBTI而不确定具体的百分比, 也可以通过以上网站进行测试获得, 或者自行评估.<br><br>注意: 全部选择中庸(50%) 并<strong>不会给你带来任何匹配优势</strong> (反而可能带来劣势).</div>" />
                <SliderElement name="mbti_ei" label="在MBTI“能量来源”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>E (外向)</p>
    <p>I (内向)</p>
    </div>" />
                <SliderElement name="mbti_sn" label="在MBTI“感知偏好”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>S (实感)</p>
    <p>N (直觉)</p>
    </div>" />
                <SliderElement name="mbti_tf" label="在MBTI“判断偏好”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>T (思考)</p>
    <p>F (情感)</p>
    </div>" />
                <SliderElement name="mbti_jp" label="在MBTI“行为模式”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>J (判断)</p>
    <p>P (感知)</p>
    </div>" />
                <StaticElement name="divider_2" tag="hr" top="2" />

                <StaticElement name="h2_2" tag="h2" content="你的匹配偏好" />
                <StaticElement name="h2_1" tag="h2" content="你的兴趣/ 爱好/ 想法" />
                <TagsElement name="hobbies" field-name="兴趣爱好" :close-on-select="false" :items="[
                    {
                        value: 'workout',
                        label: '健身',
                    },
                    {
                        value: 'read',
                        label: '阅读',
                    },
                    {
                        value: 'film',
                        label: '看剧、电影',
                    },
                    {
                        value: 'music',
                        label: '音乐',
                    },
                    {
                        value: 'travel',
                        label: '旅游',
                    },
                    {
                        value: 'photography',
                        label: '摄影',
                    },
                    {
                        value: 'acg',
                        label: '二次元',
                    },
                    {
                        value: 'vediogame',
                        label: '游戏',
                    },
                    {
                        value: 'sport',
                        label: '运动',
                    },
                    {
                        value: 'cook',
                        label: '做饭',
                    },
                    {
                        value: 'paint',
                        label: '绘画',
                    },
                    {
                        value: 'create',
                        label: '创作',
                    },
                ]" :native="false" label="选择你的爱好（多选）" :rules="['required']" :max="3" info="最多选择3个" />
                <RadiogroupElement name="travel_destination" field-name="期待的旅游地点" view="blocks" :items="[
                    {
                        value: 'sea',
                        label: '海边 ',
                        description: null,
                    },
                    {
                        value: 'town',
                        label: '安静宜人的小镇',
                        description: null,
                    },
                    {
                        value: 'city',
                        label: '现代化大都市',
                        description: null,
                    },
                    {
                        value: 'none',
                        label: '我不喜欢旅游',
                        description: null,
                    },
                ]" label="你更期待前往哪里旅游？
    " :rules="['required']" />
                <RadiogroupElement name="superpower" field-name="希望拥有的超能力" view="blocks" :items="[
                    {
                        value: 'animal',
                        label: '能和所有动物交流',
                        description: null,
                    },
                    {
                        value: 'fly',
                        label: '可以飞',
                        description: null,
                    },
                    {
                        value: 'mindreading',
                        label: '读心术',
                        description: null,
                    },
                    {
                        value: 'prophecy',
                        label: '可以预知1小时后的未来',
                        description: null,
                    },
                    {
                        value: 'resurrection',
                        label: '可以复活一次',
                        description: null,
                    },
                ]" label="你最希望拥有哪种超能力？" :rules="['required']" />
                <RadiogroupElement name="use_of_money" field-name="如何处理意外财富" view="blocks" :items="[
                    {
                        value: 'invest',
                        label: '投资理财',
                        description: null,
                    },
                    {
                        value: 'one_off',
                        label: '旅行或购买心仪已久的东西',
                        description: null,
                    },
                    {
                        value: 'save',
                        label: '储蓄起来，以备不时之需',
                        description: null,
                    },
                    {
                        value: 'daily',
                        label: '摊开用来增加日常开销',
                        description: null,
                    },
                    {
                        value: 'charity',
                        label: '捐赠给需要帮助的人',
                        description: null,
                    },
                ]" label="面对一笔意外的财富，你会？" :rules="['required']" />
                <RadiogroupElement name="family" field-name="原生家庭的重要性" view="blocks" :items="[
                    {
                        value: 2,
                        label: '很重要，而且很难改变',
                        description: null,
                    },
                    {
                        value: 1,
                        label: '重要，但是我们可以重塑自己',
                        description: null,
                    },
                    {
                        value: 0,
                        label: '不重要，主要取决于自身',
                        description: null,
                    },
                ]" label="你觉得原生家庭对一个人的影响？" :rules="['required']" />
                <RadiogroupElement name="lifestyle" field-name="最喜欢的时代" view="blocks" :items="[
                    {
                        value: 'potter',
                        label: '哈利波特',
                        description: null,
                    },
                    {
                        value: '1984',
                        label: '1984',
                        description: null,
                    },
                    {
                        value: 'prince',
                        label: '小王子',
                        description: null,
                    },
                    {
                        value: 'matrix',
                        label: '黑客帝国',
                        description: null,
                    },
                    {
                        value: 'jurassic',
                        label: '侏罗纪公园',
                        description: null,
                    },
                    {
                        value: 'gatsby',
                        label: '了不起的盖茨比',
                        description: null,
                    },
                ]" label="你更愿意在哪个书或电影中生活一段时间？" :rules="['required']" />
                <StaticElement name="divider_3" tag="hr" top="2" />

                <StaticElement name="h3_2" tag="h3" content="硬性要求" />
                <StaticElement name="p_1" tag="p"
                    content="<div>对于硬性要求, 我们将<strong>过滤掉</strong>不符合的人选<br>以下选项<strong>会减少</strong>你可匹配的人选数量.</div>" />
                <RadiogroupElement name="preferred_sex" field-name="期望对方性别" view="tabs" :items="[
                    {
                        value: 'M',
                        label: '男',
                    },
                    {
                        value: 'F',
                        label: '女',
                    },
                ]" label="你要求对方的性别是" :rules="['required']" />
                <CheckboxgroupElement name="preferred_grades" field-name="期望对方年级" view="blocks" :items="[
                    {
                        value: 'UG1',
                        label: '本科大一',
                        description: null,
                    },
                    {
                        value: 'UG2',
                        label: '本科大二',
                        description: null,
                    },
                    {
                        value: 'UG3',
                        label: '本科大三',
                        description: null,
                    },
                    {
                        value: 'UG4',
                        label: '本科大四',
                        description: null,
                    },
                    {
                        value: 'UG5',
                        label: '本科大五',
                        description: null,
                    },
                    {
                        value: 'MS',
                        label: '硕士生',
                        description: null,
                    },
                    {
                        value: 'PHD',
                        label: '博士生',
                        description: null,
                    },
                    {
                        value: 'PROF',
                        label: '教授',
                        description: null,
                    },
                ]" label="你接受对方的年级是（多选）" :rules="['required']" />
                <CheckboxgroupElement name="preferred_schools" field-name="期望对方就读学校" view="blocks" :items="[
                    {
                        value: 'HKU',
                        label: 'HKU',
                        description: null,
                    },
                    {
                        value: 'CUHK',
                        label: 'CUHK',
                        description: null,
                    },
                    {
                        value: 'UST',
                        label: 'HKUST',
                        description: null,
                    },
                ]" label="你接受对方的学校是（多选）" :rules="['required']" />
                <SliderElement name="max_time_difference" field-name="最大时差" label="你能接受的最大时差" :default="3" :min="0"
                    :max="12" :step="1" :format="{
                        suffix: ' 小时', decimals: 0,
                    }" :rules="['required']" before="<div style='margin-block: 1.5rem;'></div>" size="lg" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem; font-size: 0.875em;'>
                    <p>不接受任何时差</p>
                    <p>地球另一面也行</p>
                    </div>" />
                <RadiogroupElement name="same_location_only" field-name="地区匹配偏好" view="tabs" :items="[
                    { value: true, label: '同地区' },
                    { value: false, label: '无所谓' },
                ]" label="你要求对方的位置" :rules="['required']" info="深圳/中国/亚洲 会被看作三个不同的地区" />
                <StaticElement name="divider_4" tag="hr" top="1" bottom="1" />
                <StaticElement name="h3_3" tag="h3" content="软性要求" />
                <StaticElement name="p_3" tag="p"
                    content="<div>对于软性要求, 你可能匹配到不符合你的选择的人选<br>以下选项<strong>不会减少</strong>你可匹配的人选数量<br><br>请注意:<br>全部选项选择「无偏好」<strong>不会给你带来任何匹配优势</strong> (反而会造成劣势).</div>" />
                <RadiogroupElement name="preferred_mbti_ei" field-name="期望对方能量来源" view="tabs" :items="[
                    {
                        value: 'e',
                        label: 'E 外向',
                    },
                    {
                        value: 'x',
                        label: '无偏好',
                    },
                    {
                        value: 'i',
                        label: 'I 内向',
                    },
                ]" label="在MBTI“能量来源”维度中，你更希望对方是 " :rules="['required']" />
                <RadiogroupElement name="preferred_mbti_sn" field-name="期望对方感知偏好" view="tabs" :items="[
                    {
                        value: 's',
                        label: 'S 实感',
                    },
                    {
                        value: 'x',
                        label: '无偏好',
                    },
                    {
                        value: 'n',
                        label: 'N 直觉',
                    },
                ]" label="在MBTI“感知偏好”维度中，你更希望对方是" :rules="['required']" />
                <RadiogroupElement name="preferred_mbti_tf" field-name="期望对方判断偏好" view="tabs" :items="[
                    {
                        value: 't',
                        label: 'T 思考',
                    },
                    {
                        value: 'x',
                        label: '无偏好',
                    },
                    {
                        value: 'f',
                        label: 'F 情感 ',
                    },
                ]" label="在MBTI“判断偏好”维度中，你更希望对方是" :rules="['required']" />
                <RadiogroupElement name="preferred_mbti_jp" field-name="期望对方认知态度" view="tabs" :items="[
                    {
                        value: 'j',
                        label: 'J 判断',
                    },
                    {
                        value: 'x',
                        label: '无偏好',
                    },
                    {
                        value: 'p',
                        label: 'P 感知',
                    },
                ]" label="在MBTI“认知态度”维度中，你更希望对方是" :rules="['required']" />
                <StaticElement name="divider_6" tag="hr" top="1" bottom="1" />
                <StaticElement name="h3_4" tag="h3" content="心仪的人" />
                <TextElement name="preferred_wxid" label="如果你有想匹配的人，请留下ta的微信号"
                    description="（请注意，这并不保证100%成功，前提是对方也希望与你匹配）请确定微信号填写正确，且可被添加，请留下微信号而非电话号码，若有一方留下电话号码，而另一方留下微信号，系统将不能成功匹配."
                    :rules="['max:50']" />
                <RadiogroupElement name="continue_match" field-name="是否继续匹配" view="tabs" label="如果和ta匹配失败，是否愿意继续随机匹配"
                    :rules="['required']" :conditions="[['preferred_wxid', 'not_empty']]" :items="[
                        {
                            value: true,
                            label: '是',
                        },
                        {
                            value: false,
                            label: '否',
                        },
                    ]" />
                <StaticElement name="divider_5" tag="hr" top="2" />

                <StaticElement name="h2_3" tag="h2" content="留言" />
                <StaticElement name="h3_11" tag="h3" content="简单介绍自己" />
                <TextareaElement name="message_to_partner" label="给对方的留言"
                    placeholder="这段话将在匹配成功后展示给对方. 请不要在此留下你的联系方式, 否则将会被退出活动且押金将不予退还" :rows="5"
                    :rules="['max:50', 'min:10', 'required']" description="最少输入10个字符, 最多输入50个字符" />
                <StaticElement name="divider_7" tag="hr" top="1" bottom="1" />
                <StaticElement name="h3_6" tag="h3" content="写给主办方" />
                <TextareaElement name="comment" label="还有什么想补充的吗?"
                    placeholder="请注意, 我们无法得知申请者的外貌/ 身高/ 性格等信息, 也无法根据此进行匹配" :rows="5" />
                <CheckboxElement name="confirm1" field-name="信息无误"
                    text="我确认所填写的信息准确无误, 由信息填写错误而导致的任何问题, 我将负全部责任. 如果因为填写错误导致对方要求退出, 我的押金将完全 [不退还]" :submit="false"
                    :rules="['accepted']" />
                <CheckboxElement name="confirm2" field-name="重新提交须知" :submit="false" :rules="['accepted']"
                    text="我的申请将会与我的微信绑定, 在申请截止前我可以随时修改我的申请, 只有最新的提交会被保存. 一旦申请截止, 我将不能再次修改我的申请." />
                <StaticElement name="divider_8" tag="hr" top="2" />
            </FormElements>

            <FormStepsControls />
        </template>
    </Vueform>
</template>

<script setup lang="ts">
const form$: Ref<null | VueformInstance> = ref(null);
const router = useRouter();
const { setApplicationFormData, getApplicationFormData, deleteApplicationFormData } = useStore();
const { post } = useRequest();

// detect user's timezone and return the closest UTC offset
const defaultTimezone = computed(() => {
    const offsetMinutes = -new Date().getTimezoneOffset();
    const offsetHours = offsetMinutes / 60;

    // Format the offset as a string
    let timezoneStr: string;
    if (offsetHours >= 0) {
        timezoneStr = `UTC+${offsetHours}`;
    } else {
        timezoneStr = `UTC${offsetHours}`;
    }

    return timezoneStr;

});

// Load saved form data when component mounts
onMounted(() => {
    const savedData = getApplicationFormData();
    if (savedData) {
        // Use nextTick to ensure form is fully initialized
        nextTick(() => {
            if (form$.value) {
                form$.value.load(savedData);
            }
        });
    }
});

async function handleSubmit(form: VueformInstance, formData: any) {
    form.submitting = true;
    const data = form.data;
    if (data.continue_match === null) {
        data.continue_match = true;
    }

    try {
        const res = await post("applicants/", data);

        if (res.status === 403) {
            alert("你已经退出了活动，无法再次报名");
            router.push("/");
            return;
        }
        if (!res.ok) {
            const errorData = await res.json();
            throw new Error(errorData.detail || `报名失败: ${res.statusText}`);
        }

        const responseData = await res.json();
        if (responseData.data.paid) {
            router.push("/");
        } else {
            router.push("/payment");
        }
    } catch (err: any) {
        alert(err.message);
        console.error(err);
    } finally {
        form.submitting = false;
    }
}

function updateData(data: any) {
    // Save form data to localStorage whenever form changes
    if (data) {
        setApplicationFormData(data);
    }
};
</script>

<style scoped>
.vf-application-form *,
.vf-application-form *:before,
.vf-application-form *:after,
.vf-application-form:root {
    --vf-primary: var(--clr-primary);
    --vf-primary-darker: var(--clr-primary-dark);
    --vf-color-on-primary: #ffffff;

    --vf-color-passive: var(--clr-text--muted);

    /* slider */
    --vf-ring-width: 2px;
    --vf-ring-color: var(--clr-primary-light);
    --vf-slider-handle-size-lg: 1.75rem;

    --vf-font-size-h1: 2.125rem;
    --vf-font-size-h2: 1.875rem;
    --vf-font-size-h3: 1.5rem;
    --vf-font-size-h1-mobile: var(--fs-600);
    --vf-font-size-h2-mobile: var(--fs-600);
    --vf-font-size-h3-mobile: var(--fs-500);

    --vf-line-height: 1.5;
    --vf-line-height-headings: 1.2;
}

</style>