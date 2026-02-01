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
                    'major',
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
                    'p_14',
                    'hobbies',
                    'fav_movies',
                    'wish',
                    'why_lamp_remembered_your_name',
                    'weekend_arrangement',
                    'reply_frequency',
                    'expectation',
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
                    'h2_5',
                    'p_15',
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
                    <li class='vf-li'>2月1日19:00 PM - 开始报名</li>
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
                <br>
                <p>若你希望通过微信<strong>收到匹配结果以及每日任务截止提醒</strong>, 请扫码关注 Triple Uni 公众号</p>
                <img src='/imgs/uni_qrcode.webp' style='margin: 1rem auto; width: 80%;'>

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
                    <li class='vf-li'>70元: 完成每日主线任务 (10元/天)</li>
                    <li class='vf-li'>20元: 完成3天的主线任务</li>
                    <li class='vf-li'>9元: 完成结束反馈问卷</li>
                </ul>
                <strong>若完成的主线任务不足3天, 则所有押金将不予退还</strong><br>
                <br>
                押金将在报名时收取, <strong>只有成功缴纳才视为报名完成.</strong><br>
                在报名截止前, 你可以随时选择退出活动并获得全额退款. 报名截止后, 你必须完成所有基础活动内容方可获得押金退还.<br>
                <br>
                如果因为对方原因导致无法继续活动, 请及时联系你的Mentor并说明情况, 我们将会视情况为你做出安排<br>
                <br>
                押金将在活动结束后30日内原路退还.关于押金退还规则的解释权归主办方所有.<br>
            </div>" />
                <StaticElement name="h3_10" tag="h3" content="数据收集 & 隐私承诺" top="2" />
                <StaticElement name="p_8" tag="p" content="
            <div>
                我们将会收集并保存以下隐私信息:<br>
                <br>
                [通过微信登录授权]<br>
                <ul>
                    <li class='vf-li'>你的微信头像</li>
                    <li class='vf-li'>你的微信昵称</li>
                    <li class='vf-li'>你的微信OpenID (用作网站登录, 微信支付)</li>
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
                <strong>你的任务将由我们部署在私有云上的人工智能模型自动评分, 我们不使用第三方的AI服务提供商, 以最大程度确保你的隐私. 在没有你的允许下Mentor无法看到你提交的内容. 为了确保能够准确评分, 请不要遮挡/ 修改/ 模糊你提交的任务.</strong><br>
            </div>" />
                <StaticElement name="h3_12" tag="h3" content="故障自助处理" top="2" />
                <StaticElement name="p_9" tag="p"
                    content="<div>如果你在网站上遇到了错误, 可以尝试以下步骤修复:<br><br> 1. 打开网站首页<br> 2. 点击左上方的「?」 标签<br> 3. 点击「清除页面缓存」按钮<br> 4. 重新登录</div>" />
                <StaticElement name="divider" tag="hr" top="2" />
                <CheckboxElement name="checkbox" field-name="规则及隐私条款" :rules="['accepted']" :disabled="formDisabled"
                    text="我已详细阅读、理解并同意以上所有内容以及<a href='/agreement'>《一周CP2026协议书》</a>并愿意参加活动." :submit="false" />




                <StaticElement name="h2" tag="h2" content="个人信息" />
                <StaticElement name="h3" tag="h3" content="基础信息" />
                <TextElement name="name" field-name="姓名" label="你的中文全名" placeholder="张三" :rules="['required', 'max:4']"
                    :disabled="formDisabled" />
                <TextElement name="wxid" field-name="微信号" :columns="{
                    label: 12,
                    wrapper: 12,
                }" :rules="['required', 'max:50']" label="你的微信号" :disabled="formDisabled"
                    description="请确定wxid正确，且可被搜索/ 添加. 如果你的微信号是以wxid开头的原始id，请填入手机号." placeholder="my_wechat_id" />
                <RadiogroupElement name="sex" field-name="性别" view="tabs" :items="[
                    {
                        value: 'M',
                        label: '男',
                    },
                    {
                        value: 'F',
                        label: '女',
                    },
                ]" label="你的性别" :rules="['required']" :disabled="formDisabled" />
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
                ]" label="你就读的学校" :rules="['required']" :disabled="formDisabled" />
                <TextElement name="major" field-name="专业" label="你的专业" :rules="['required', 'max:50']"
                    :disabled="formDisabled" />
                <TextElement name="email" input-type="email" :rules="[
                    'regex:^[a-zA-Z0-9._%+-]+@(connect\\.ust\\.hk|connect\\.hku\\.hk|link\\.cuhk\\.edu\\.hk)$',
                    'email',
                    'required'
                ]" label="你的学校邮箱" placeholder="email@example.com" description="我们会发送验证码至此邮箱以验证归属, 请确认邮箱填写正确"
                    :disabled="formDisabled" />
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
                    {
                        value: 'GRAD',
                        label: '已毕业',
                        description: null,
                    },
                ]" label="你目前的年级" :rules="['required']" :disabled="formDisabled" />
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
                ]" label="你所在的时区" placeholder="选择你的时区" :default="defaultTimezone" :rules="['required']"
                    :disabled="formDisabled" />
                <SelectElement name="location" field-name="所在地区" :native="false" :items="[
                    { value: 'HK', label: '香港' },
                    { value: 'SZ', label: '深圳' },
                    { value: 'GD', label: '广东省' },
                    { value: 'TW', label: '台湾省' },
                    { value: 'CN', label: '中国' },
                    { value: 'JP_KR', label: '日韩' },
                    { value: 'ASIA', label: '亚洲' },
                    { value: 'OCEANIA', label: '大洋洲' },
                    { value: 'UK', label: '英国' },
                    { value: 'EU', label: '欧洲' },
                    { value: 'US', label: '美国' },
                    { value: 'CA', label: '加拿大' },
                    { value: 'NA', label: '北美洲' },
                    { value: 'OTHER', label: '其他' },
                ]" label="你本学期最常在的地区" :rules="['required']" :disabled="formDisabled"
                    description="请选择<strong>最精确(小)的选项</strong>. 如果你在多个地区之间频繁往返，请选择你待的时间最长的地区." />
                <StaticElement name="divider_1" tag="hr" top="1" bottom="1" />
                <StaticElement name="h3_1" tag="h3" content="MBTI 性格测试结果" />
                <StaticElement name="p" tag="p" :content="`<div>
                        请通过滑动的方式选择你的MBTI.<br>
                        <br>
                        如果你不确定自己的MBTI, 可以通过 <a href='https://www.16personalities.com\' target='blank'>https://www.16personalities.com (免费)</a><br>
                        或其他网站进行测试.<br>
                        <br>别害怕! 你可以做完整个测试后再回来继续填写, <strong>所有进度将会被自动保存.</strong><br>
                        <br>
                        如果你只知道自己的MBTI而不确定具体的百分比, 也可以通过以上网站进行测试获得, 或者自行评估.<br>
                        <br>
                        注意: 全部选择中庸(50%) 并<strong>不会给你带来任何匹配优势</strong> (反而可能带来劣势).<br>
                        <br>
                        你设置的MBTI为: <strong>${userMBTI}</strong><br>
                    </div>`" />
                <SliderElement name="mbti_ei" label="在MBTI“能量来源”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>E (外向)</p>
    <p>I (内向)</p>
    </div>" :disabled="formDisabled" />
                <SliderElement name="mbti_sn" label="在MBTI“感知偏好”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>S (实感)</p>
    <p>N (直觉)</p>
    </div>" :disabled="formDisabled" />
                <SliderElement name="mbti_tf" label="在MBTI“判断偏好”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>T (思考)</p>
    <p>F (情感)</p>
    </div>" :disabled="formDisabled" />
                <SliderElement name="mbti_jp" label="在MBTI“行为模式”维度中，你认为自己更偏向" :default="50" show-tooltip="drag" :min="0"
                    :max="100" :step="1" :format="{
                        suffix: '%',
                    }" size="lg" :rules="['required']" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem;'>
    <p>J (判断)</p>
    <p>P (感知)</p>
    </div>" :disabled="formDisabled" />
                <StaticElement name="divider_2" tag="hr" top="2" />




                <StaticElement name="h2_1" tag="h2" content="你的兴趣/ 爱好/ 想法" />
                <StaticElement name="p_14" tag="p" content="此页内容仅用于匹配, 不会有任何人, 包括你的CP与Mentor, 能够看到你的答案, 请放心填写." />
                <TagsElement name="hobbies" :close-on-select="false" :search="true" autocomplete="off" :create="true"
                    placeholder="通过换行添加, 最多五个" :floating="false" :append-new-option="false" :max="5" label="你有什么兴趣爱好"
                    :rules="[
                        'required',
                    ]" :caret="false" :items="hobbiesItems" :disabled="formDisabled"
                    description='可以是抽象的概念, 例如"旅游"、"读书". 也可以是某个活动, 例如"双板滑雪"、"胶卷摄影". 如果你有具体喜欢的游戏, 则可以写上游戏名,例如"王者荣耀".' />
                <TagsElement name="fav_movies" :close-on-select="false" :search="true" label="你最喜欢的书/ 电影/ 动漫/ 电视剧"
                    autocomplete="off" :create="true" placeholder="通过换行添加, 最多五个" :floating="false"
                    :append-new-option="false" :max="5" :rules="[
                        'required',
                    ]" :caret="false" :items="favMoviesItems" :disabled="formDisabled" />
                <TextareaElement name="wish" :floating="false" :rows="3" :rules="[
                    'required',
                    'min:5',
                    'max:50',
                ]" description="不受任何限制的话, 你最想要做的是什么呢? (5-50字)" placeholder="因为是盗版的阿拉丁所以只能实现一个愿望...
但是放心不会有副作用啦~" label='你拿到了"阿拉丙神灯"会许什么愿望' :addons="{
    after: '<div class=\&#39;word-count\&#39;>(0)</div>',
}" :disabled="formDisabled" />
                <TextareaElement name="why_lamp_remembered_your_name" :floating="false" :rows="3" :rules="[
                    'required',
                    'min:5',
                    'max:50',
                ]" description="你觉得为什么楼下的路灯会记住你的名字? (5-50字)" placeholder="这是一个脑洞问题, 请尽情发挥想象力!"
                    label="你觉得为什么楼下的路灯会记住你的名字?" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <TextareaElement name="weekend_arrangement" :floating="false" :rows="3" :rules="[
                    'required',
                    'min:5',
                    'max:50',
                ]" description="假设你没有作业, Project, 考试或者其他事情限制你, 你会做什么呢? (5-50字)" placeholder='描述你预想中的周末
' label="自由安排这个周末你会做什么" :addons="{
    after: '<div class=\&#39;word-count\&#39;>(0)</div>',
}" :disabled="formDisabled" />
                <RadiogroupElement name="reply_frequency" :items="[
                    {
                        value: '5',
                        label: '一直在线, 基本秒回',
                    },
                    {
                        value: '4',
                        label: '经常看手机, 看到就回',
                    },
                    {
                        value: '3',
                        label: '佛系查看, 不定时回复',
                    },
                    {
                        value: '2',
                        label: '攒很多消息, 逐一回复',
                    },
                    {
                        value: '1',
                        label: '开启勿扰模式, 闲下来再回',
                    },
                ]" label="你的聊天习惯是" :rules="['required']" size="md" :disabled="formDisabled" />
                <TextareaElement name="expectation" :floating="false" :rows="3" :rules="[
                    'required',
                    'min:10',
                    'max:50',
                ]" description="只是希望单纯交个朋友, 还是认真地希望进入一段关系?  是饭搭子, 网友还是恋人? 会考虑长期关系吗? (10-50字)" placeholder='描述你参加活动的目的以及想法
' label="你期待与CP的关系是什么" :addons="{
    after: '<div class=\&#39;word-count\&#39;>(0)</div>',
}" :disabled="formDisabled" />
                <StaticElement name="divider_3" tag="hr" top="2" />



                <StaticElement name="h2_2" tag="h2" content="你的匹配偏好" />
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
                ]" label="你要求对方的性别是" :rules="['required']" :disabled="formDisabled" />
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
                    {
                        value: 'GRAD',
                        label: '已毕业',
                        description: null,
                    },
                ]" label="你接受对方的年级是（多选）" :rules="['required']" :disabled="formDisabled" />
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
                ]" label="你接受对方的学校是（多选）" :rules="['required']" :disabled="formDisabled" />
                <SliderElement name="max_time_difference" field-name="最大时差" label="你能接受的最大时差" :default="3" :min="0"
                    :max="12" :step="1" :format="{
                        suffix: ' 小时', decimals: 0,
                    }" :rules="['required']" before="<div style='margin-block: 1.5rem;'></div>" size="lg" after="<div style='display:flex; margin-block: 0.5rem 0.5rem; justify-content: space-between; padding-inline: 0.5rem; font-size: 0.875em;'>
                    <p>不接受任何时差</p>
                    <p>地球另一面也行</p>
                    </div>" :disabled="formDisabled" />
                <RadiogroupElement name="same_location_only" field-name="地区匹配偏好" view="tabs" :items="[
                    { value: true, label: '同地区' },
                    { value: false, label: '无所谓' },
                ]" label="你要求对方的位置" :rules="['required']" info="深圳/中国/亚洲 会被看作三个不同的地区" :disabled="formDisabled" />
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
                ]" label="在MBTI“能量来源”维度中，你更希望对方是 " :rules="['required']" :disabled="formDisabled" />
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
                ]" label="在MBTI“感知偏好”维度中，你更希望对方是" :rules="['required']" :disabled="formDisabled" />
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
                ]" label="在MBTI“判断偏好”维度中，你更希望对方是" :rules="['required']" :disabled="formDisabled" />
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
                ]" label="在MBTI“认知态度”维度中，你更希望对方是" :rules="['required']" :disabled="formDisabled" />
                <StaticElement name="divider_6" tag="hr" top="1" bottom="1" />
                <StaticElement name="h3_4" tag="h3" content="心仪的人" />
                <TextElement name="preferred_wxid" label="如果你有想匹配的人，请留下ta的微信号"
                    description="（请注意，这并不保证100%成功，前提是对方也希望与你匹配）请确定微信号填写正确，且可被添加，请留下微信号而非电话号码，若有一方留下电话号码，而另一方留下微信号，系统将不能成功匹配."
                    :rules="['max:50']" :disabled="formDisabled" />
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
                    ]" :disabled="formDisabled" />
                <StaticElement name="divider_5" tag="hr" top="2" />



                <StaticElement name="h2_3" tag="h2" content="留言" />
                <StaticElement name="h3_11" tag="h3" content="简单介绍自己" />
                <TextareaElement name="message_to_partner" label="给对方的留言"
                    placeholder="这段话将在匹配成功后展示给对方. 请不要在此留下你的联系方式, 否则将会被退出活动且押金将不予退还" :rows="5"
                    :rules="['max:50', 'min:10', 'required']" description="最少输入10个字符, 最多输入50个字符" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <StaticElement name="divider_7" tag="hr" top="1" bottom="1" />
                <StaticElement name="h2_5" tag="h3" content="关于通知" />
                <StaticElement name="p_15" tag="p" content="
                <div>
                    <p>若你希望通过微信<strong>收到匹配结果以及每日任务截止提醒</strong>, 请扫码关注 Triple Uni 公众号</p>
                    <img src='/imgs/uni_qrcode.webp' style='margin: 1rem auto; width: 80%;'>

                </div>" />
                <StaticElement name="h3_6" tag="h3" content="写给主办方" />
                <TextareaElement name="comment" label="还有什么想补充的吗?"
                    placeholder="请注意, 我们无法得知申请者的外貌/ 身高/ 性格等信息, 也无法根据此进行匹配" :rows="5" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <CheckboxElement name="confirm1" field-name="信息无误"
                    text="我确认所填写的信息准确无误, 由信息填写错误而导致的任何问题, 我将负全部责任. 如果因为填写错误导致对方要求退出, 我的押金将完全 [不退还]" :submit="false"
                    :rules="['accepted']" :disabled="formDisabled" />
                <CheckboxElement name="confirm2" field-name="重新提交须知" :submit="false" :rules="['accepted']"
                    text="我的申请将会与我的微信绑定, 在申请截止前我可以随时修改我的申请, 只有最新的提交会被保存. 一旦申请截止, 我将不能再次修改我的申请."
                    :disabled="formDisabled" />
                <StaticElement name="divider_8" tag="hr" top="2" :disabled="formDisabled" />
            </FormElements>

            <FormStepsControls />
        </template>
    </Vueform>
</template>

<script setup lang="ts">
const form$: Ref<null | VueformInstance> = ref(null);
const router = useRouter();
const { setApplicationFormData, getApplicationFormData, deleteApplicationFormData } = useStore();
const { get, post } = useRequest();
const hobbiesItems = computed(() => {
    return form$.value?.data.hobbies || [];
});
const favMoviesItems = computed(() => {
    return form$.value?.data.fav_movies || [];
});
const formDisabled = computed(() => {
    if (
        userState.value === UserStates.APPLICATION_START ||
        userState.value === UserStates.APPLIED ||
        userState.value === UserStates.PAID
    ) {
        return false;
    }
    return true;
});

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

const userMBTI = computed(() => {
    const mbti = getMBTIType({
        ei: form$.value?.data.mbti_ei,
        sn: form$.value?.data.mbti_sn,
        tf: form$.value?.data.mbti_tf,
        jp: form$.value?.data.mbti_jp,
    });
    return mbti;
});

// Load saved form data when component mounts
onMounted(async () => {
    const textareaContainers = document.querySelectorAll('.vf-input-group-textarea');
    textareaContainers.forEach(container => {
        const textarea = container.querySelector('textarea');
        if (textarea) {
            const wordCountElement = container.querySelector('.word-count');

            const observer = new MutationObserver(() => {
                const wordCount = textarea.value.length;
                if (wordCountElement) {
                    wordCountElement.textContent = `(${wordCount})`;
                }
            });
            observer.observe(textarea, { attributes: true, attributeFilter: ['value'] });

        }
    });

    let savedData = getApplicationFormData();
    if (
        userState.value !== UserStates.APPLICATION_START
    ) {
        try {
            const res = await get("applicants/");
            if (res.ok) {
                const responseData = await res.json();
                savedData = responseData.data.form_data;
                savedData.checkbox = true;
                savedData.confirm1 = true;
                savedData.confirm2 = true;
            }
            else if (res.status === 403) {
                alert("你已经退出了活动");
                router.push("/");
                return;
            }
            else {
                const errorData = await res.json();
                console.error(errorData);
                throw new Error(errorData.detail || "获取表单数据失败: " + res.status);
            }
        } catch (err: any) {
            alert(err.message);
            console.error(err);
        }
    }

    if (savedData) {
        if (form$.value) {
            form$.value.load(savedData);
        }
    }

});

async function handleSubmit(form: VueformInstance, formData: any) {

    if (formDisabled.value) {
        return
    }

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
            console.error(errorData);
            if (errorData.detail) {
                throw new Error(errorData.detail);
            }
            else if (typeof errorData === "object") {
                let errorMessage = "";
                Object.entries(errorData).forEach(([field, message]) => {
                    errorMessage += `${field}: ${message}\n`;
                });
                throw new Error(errorMessage);
            }
            throw new Error(`报名失败: ${res.status}`);
        }

        const responseData = await res.json();
        if (responseData.data.paid) {
            router.push("/");
        } else {
            await fetchUserState();
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

<style>
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

#hobbies-dropdown,
#fav_movies-dropdown {
    display: none;
}

.vf-input-group-textarea {
    position: relative;
}

.vf-input-group-textarea .word-count {
    position: absolute;
    right: 0.5rem;
    bottom: 0;
    font-family: monospace;
    letter-spacing: -2px;
    font-size: var(--fs-200);
    color: var(--clr-text--muted);
}
</style>