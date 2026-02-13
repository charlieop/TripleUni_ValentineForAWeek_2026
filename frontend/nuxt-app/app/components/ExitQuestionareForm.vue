<template>
    <Vueform size="md" :endpoint="false" validate-on="step" :float-placeholders="false"
        add-class="vf-exit-questionnaire-form" ref="form$" @change="updateData" :onSubmit="handleSubmit">
        <template #empty>
            <FormSteps>
                <FormStep name="page0" :elements="[
                    'page_title',
                    'intro_text',
                    'divider_intro',
                ]" label="开始" />
                <FormStep name="page1" label="匹配与任务" :elements="[
                    'h2_matching',
                    'matching_satisfaction',
                    'matching_unsatisfied_reason',
                    'matching_suggestion',
                    'divider_1',
                    'h2_tasks',
                    'task_pace',
                    'favorite_task',
                    'least_favorite_task',
                    'task_suggestion',
                    'day7_letter_rating',
                    'divider_2',
                ]" />
                <FormStep name="page2" label="关于你们" :elements="[
                    'h2_about_pair',
                    'heartbeat_moment',
                    'knew_before',
                    'interaction_frequency',
                    'interaction_frequency_other',
                    'future_relationship',
                    'future_relationship_other',
                    'partner_engagement',
                    'self_engagement',
                    'partner_comment',
                    'divider_3',
                ]" />
                <FormStep name="page3" label="结束" :elements="[
                    'h2_letter',
                    'message_to_partner',
                    'divider_4',
                    'h2_callback',
                    'lamp_callback',
                    'divider_5',
                    'h2_other',
                    'participated_last_year',
                    'comparison_rating',
                    'comparison_comment',
                    'discovery_channel',
                    'discovery_channel_other',
                    'recommendation_likelihood',
                    'mentor_rating',
                    'accept_callback',
                    'message_to_organizer',
                    'divider_6',
                ]" />
            </FormSteps>

            <FormElements>
                <!-- ========== Page 0: 开始 ========== -->
                <StaticElement name="page_title" tag="h1" content="Triple Uni 一周CP 结束问卷" />
                <StaticElement name="intro_text" tag="p" content="
                <div class='intro-text'>
                    Triple Uni“情人节”特别专列即将到站，<br>
                    七日的CP旅程已然悄然走向尾声。<br>
                    不知你是否还记得，<br>
                    打出第一段话时内心的激动与紧张？<br>
                    <br>
                    是否还想起共同完成任务时的满满成就，<br>
                    是否还回味字里行间洋溢着的温度，<br>
                    抑或是<br>
                    这又只是一场令人心生沮丧的闹剧？<br>
                    <br>
                    不论你在这七天内有何感想，<br>
                    失落还是雀跃，<br>
                    沉默还是滔滔不绝，<br>
                    命运都曾在某一个不经意的瞬间，<br>
                    让两条原本平行的轨迹，<br>
                    短暂地靠近，<br>
                    并肩穿过一段只属于彼此的光阴。<br>
                    <br>
                    当列车缓缓停靠，<br>
                    请带走属于你的那一份故事。<br>
                    无论它是未完的序章，<br>
                    还是温柔的句点。<br>
                    <br>
                    愿你在未来的某一天，<br>
                    再次想起这趟旅程时，<br>
                    不是遗憾，<br>
                    而是会在心底轻声说：<br>
                    “曾有一周，<br>
                    命运将我们写进同一行诗里。”<br>
                    <br>
                    最后，<br>
                    祝你们新春快乐，马年吉祥，<br>
                    前路灿烂，万事有光。<br>
                    <br>
                    <span class='signature'>一周CP全体工作人员</span>
                    <span class='signature'>感谢你们的参与</span>
                    <br>
                </div>" />
                <StaticElement name="divider_intro" tag="hr" />

                <!-- ========== Page 1: 关于匹配与任务 ========== -->
                <StaticElement name="h2_matching" tag="h2" align="left" content="关于匹配算法" />
                <RadiogroupElement name="matching_satisfaction" view="tabs" :items="[
                    { value: 1, label: '1' },
                    { value: 2, label: '2' },
                    { value: 3, label: '3' },
                    { value: 4, label: '4' },
                    { value: 5, label: '5' },
                ]" label="你匹配到的CP有多符合你问卷里填写的要求？" description="1-5分，分数越高即为越符合" :rules="['required']"
                    :disabled="formDisabled" />
                <TextElement name="matching_unsatisfied_reason" label="你对于匹配不满意的原因是？" :rules="['max:30']"
                    description="(0-30字)" :conditions="[
                        ['matching_satisfaction', 'in', [2, 1]],
                    ]" :disabled="formDisabled" />
                <TextareaElement name="matching_suggestion" label="你对匹配问卷/算法有任何建议或想法吗？" :rules="['min:0', 'max:100']"
                    placeholder="例如: 问卷应该额外/减少收集哪些信息?
匹配算法应该额外考虑哪些内容?" :rows="3" description="(0-100字)" :addons="{
    after: '<div class=\&#39;word-count\&#39;>(0)</div>',
}" :disabled="formDisabled" />
                <StaticElement name="divider_1" tag="hr" />

                <StaticElement name="h2_tasks" tag="h2" content="关于活动任务" />
                <RadiogroupElement name="task_pace" view="tabs" :items="[
                    { value: 0, label: '过于暧昧' },
                    { value: 1, label: '节奏刚刚好' },
                    { value: 2, label: '希望更亲近' },
                ]" label="你认为任务节奏是否合理？" :rules="['required']" :disabled="formDisabled" />
                <TextareaElement name="favorite_task" label="请告诉我们你最喜欢/印象最深刻的任务是什么？为什么？"
                    :rules="['required', 'min:5', 'max:100']" description="(5-100字)" placeholder="如果有多个的话都可以写下来~"
                    :rows="4" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <TextareaElement name="least_favorite_task" label="请告诉我们你最不喜欢/感到最尴尬的任务是什么？为什么？" description="(5-100字)"
                    :rules="['required', 'min:5', 'max:100']" placeholder="如果有多个的话都可以写下来~" :rows="4" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <TextareaElement name="task_suggestion" label="对于每天的任务设置你有什么建议吗？" placeholder="例如: 你觉得任务数量如何?
希望增加什么类型的任务呢?
希望有什么更加灵活的地方?" :rows="4" :rules="['max:100']" description="(0-100字)" :addons="{
    after: '<div class=\&#39;word-count\&#39;>(0)</div>',
}" :disabled="formDisabled" />
                <RadiogroupElement name="day7_letter_rating" view="tabs" :items="[
                    { value: 1, label: '1' },
                    { value: 2, label: '2' },
                    { value: 3, label: '3' },
                    { value: 4, label: '4' },
                    { value: 5, label: '5' },
                ]" label="你觉得对方给你写的Day7信件有多触动你？" :rules="['required']" :disabled="formDisabled" />
                <StaticElement name="divider_2" tag="hr" />

                <!-- ========== Page 2: 关于你们 ========== -->
                <StaticElement name="h2_about_pair" tag="h2" content="关于你们" />
                <TextareaElement name="heartbeat_moment" label="请向我们分享一个你本周的心动时刻："
                    :rules="['required', 'min:10', 'max:200']" :rows="5" description="(10-200字)"
                    placeholder="最喜欢与ta交流的那一个瞬间呢?" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <SelectElement name="knew_before" :items="[
                    { value: 0, label: '我们完全不认识' },
                    { value: 1, label: '我有见过/ 听说过ta但没有微信' },
                    { value: 2, label: '我有ta的微信但是并不熟' },
                    { value: 3, label: '我们是朋友来参加活动的' },
                    { value: 4, label: '我们是情侣来参加活动的' },
                ]" :search="true" :native="false" label="你们在活动前认识吗？" input-type="search" autocomplete="off"
                    :rules="['required']" :disabled="formDisabled" />
                <SelectElement name="interaction_frequency" :search="true" :native="false" input-type="search"
                    autocomplete="off" label="你们每天的互动频率是？" :items="[
                        { value: 0, label: '每天多次，感觉特别多话说' },
                        { value: 1, label: '每天几次，偶尔会聊天' },
                        { value: 2, label: '每天仅为完成任务' },
                        { value: 3, label: '有的时候一整天都没说话' },
                        { value: 4, label: '其它（请补充）' },
                    ]" :can-deselect="false" :rules="['required']" :disabled="formDisabled" />
                <TextElement name="interaction_frequency_other" :rules="[
                    {
                        required: [['interaction_frequency', 'in', [4]]],
                    },
                    'min:2',
                    'max:30',
                ]" :conditions="[
                    ['interaction_frequency', 'in', [4]],
                ]" label="请在此补充 (互动频率)" description="(2-30字)" :disabled="formDisabled" />
                <SelectElement name="future_relationship" :items="[
                    { value: 0, label: '我们已经在一起了' },
                    { value: 1, label: '我希望进一步了解ta，并考虑在一起' },
                    { value: 2, label: '我希望与ta继续做经常聊天的好朋友' },
                    { value: 3, label: '我只考虑与ta做普通朋友，偶尔联络' },
                    { value: 4, label: '我不会再主动联络ta' },
                    { value: 5, label: '我们已经没有再说话了' },
                    { value: 6, label: '其它（请补充）' },
                ]" :search="true" :native="false" input-type="search" autocomplete="off" label="在活动结束后，你们的关系会是？"
                    :can-deselect="false" :rules="['required']" :disabled="formDisabled" />
                <TextElement name="future_relationship_other" :rules="[
                    {
                        required: [['future_relationship', 'in', [6]]],
                    },
                    'min:2',
                    'max:30',
                ]" :conditions="[
                    ['future_relationship', 'in', [6]],
                ]" label="请在此补充 (与ta的关系)" description="(2-30字)" :disabled="formDisabled" />
                <SliderElement name="partner_engagement" label="你认为ta对本次活动有多投入？" description="1-10分，分数越高即越认真参与活动"
                    :min="1" :max="10" :step="1" :rules="['required']" :default="0" :disabled="formDisabled" />
                <SliderElement name="self_engagement" label="你认为自己在本次活动中有多投入？" description="1-10分，分数越高即越认真参与活动"
                    :rules="['required']" :min="1" :max="10" :step="1" :default="0" :disabled="formDisabled" />
                <TextareaElement name="partner_comment" label="关于ta, 还有什么想要补充的吗？" :rules="['max:100']"
                    description="(0-100字)" placeholder="请放心，你在这里填写的内容 不会 向对方展示" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <StaticElement name="divider_3" tag="hr" />

                <!-- ========== Page 3: 结束 ========== -->
                <StaticElement name="h2_letter" tag="h2" content="跨越时空的书信" />
                <TextareaElement name="message_to_partner" label="小小传话筒" :rules="['required', 'min:20', 'max:500']"
                    description="在7天的活动结束后，不知道你是否还有什么想对ta说的话呢？
请把你想对她说的话放在这里吧。我们会在两周之后通过邮件的方式帮你把这段话发送给ta哦！
<br>
(20-500字 )
" :rows="6" placeholder="我想对两周之后的ta说：..." :addons="{
    after: '<div class=\&#39;word-count\&#39;>(0)</div>',
}" :disabled="formDisabled" />
                <StaticElement name="divider_4" tag="hr" />

                <StaticElement name="h2_callback" tag="h2" content="Callback" />
                <TextareaElement name="lamp_callback" label="你现在知道楼下的路灯为什么会记住你的名字了吗?" :rules="['max:100']" description="(0-100字)
" :rows="3" placeholder="_(:_」∠)_" :addons="{
    after: '<div class=\&#39;word-count\&#39;>(0)</div>',
}" :disabled="formDisabled" />
                <StaticElement name="divider_5" tag="hr" />

                <StaticElement name="h2_other" tag="h2" content="其他信息" />
                <RadiogroupElement name="participated_last_year" view="tabs" :items="[
                    { value: false, label: '没有参加' },
                    { value: true, label: '有参加过' },
                ]" label="你有参加过去年的一周CP活动吗？" :disabled="formDisabled" />
                <SliderElement name="comparison_rating" label="假设上次活动的综合体验为5分，你会为这次活动打多少分？" :min="1" :max="10" :step="1"
                    :default="5" :rules="['required']" :conditions="[
                        ['participated_last_year', 'in', [true]],
                    ]" :disabled="formDisabled" />
                <TextareaElement name="comparison_comment" label="与上次活动相比，你觉得这次有什么做得更好/更不好的地方？" description="(0-100字)"
                    :rules="['max:100']" :conditions="[
                        ['participated_last_year', 'in', [true]],
                    ]" :rows="3" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <SelectElement name="discovery_channel" :items="[
                    { value: 0, label: 'Triple Uni小程序或公众号' },
                    { value: 1, label: '其他微信公众号' },
                    { value: 2, label: '朋友转发（微信聊天/朋友圈等）' },
                    { value: 3, label: '其它社交平台（小红书等）' },
                    { value: 4, label: '我本身就知道这个活动' },
                    { value: 5, label: '其它（请补充）' },
                ]" :search="true" :native="false" input-type="search" autocomplete="off" label="你是通过哪种渠道了解到我们活动的？"
                    :can-deselect="false" :rules="['required']" :disabled="formDisabled" />
                <TextElement name="discovery_channel_other" :rules="[
                    {
                        required: [['discovery_channel', 'in', [5]]],
                    },
                    'min:2',
                    'max:30',
                ]" :conditions="[
                    ['discovery_channel', 'in', [5]],
                ]" label="请在此补充 (了解渠道)" description="(2-30字)" :disabled="formDisabled" />
                <SliderElement name="recommendation_likelihood" label="你有多大可能会在明年将本活动推荐给你的朋友？" :min="0" :max="100"
                    :step="1" :rules="['required']" :default="0" :format="{ suffix: '%' }" :disabled="formDisabled" />
                <SliderElement name="mentor_rating" label="请为你的Mentor打一个分吧!" :min="1" :max="10" :step="1"
                    :rules="['required']" description="你的Mentor是否有来提醒每日任务、打分情况等？Ta是否能够及时的帮助你解决遇到的问题？"
                    :disabled="formDisabled" />
                <RadiogroupElement name="accept_callback" view="tabs" :items="[
                    { value: false, label: '不愿意' },
                    { value: true, label: '愿意' },
                ]" label="你是否愿意接受我们的回访?" description='如果你选择 "愿意"，则我们有可能在活动结束后通过微信联系你' :rules="['required']"
                    :default="true" :disabled="formDisabled" />
                <TextareaElement name="message_to_organizer" label="还有什么想对主办方说的吗？" description="(0-200字)"
                    :rules="['max:200']" :addons="{
                        after: '<div class=\&#39;word-count\&#39;>(0)</div>',
                    }" :disabled="formDisabled" />
                <StaticElement name="divider_6" tag="hr" />
            </FormElements>

            <FormStepsControls />
        </template>
    </Vueform>
</template>

<script setup lang="ts">
const form$: Ref<null | VueformInstance> = ref(null);
const router = useRouter();
const { setExitQuestionnaireFormData, getExitQuestionnaireFormData } = useStore();
const { get, post } = useRequest();

const formDisabled = computed(() => {
    if (
        userState.value === UserStates.EXIT_QUESTIONNAIRE_RELEASE
    ) {
        return false;
    }
    return true;
});

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

    let savedData = getExitQuestionnaireFormData();

    // Try to load from server if already submitted
    try {
        const res = await get("exit-questionnaire/");
        if (res.ok) {
            const responseData = await res.json();
            savedData = responseData.data.form_data;
        }
    } catch (err: any) {
        console.error(err);
    }

    if (savedData && form$.value) {
        form$.value.load(savedData);
    }
});

async function handleSubmit(form: VueformInstance, formData: any) {
    if (formDisabled.value) {
        return;
    }

    form.submitting = true;
    const data = form.data;

    try {
        const res = await post("exit-questionnaire/", data);

        if (!res.ok) {
            const errorData = await res.json();
            console.error(errorData);
            if (errorData.detail) {
                throw new Error(errorData.detail);
            } else if (typeof errorData === "object") {
                let errorMessage = "";
                Object.entries(errorData).forEach(([field, message]) => {
                    errorMessage += `${field}: ${message}\n`;
                });
                throw new Error(errorMessage);
            }
            throw new Error(`提交失败: ${res.status}`);
        }

        alert("提交成功！感谢你的反馈！");
        router.push("/");
    } catch (err: any) {
        alert(err.message);
        console.error(err);
    } finally {
        form.submitting = false;
    }
}

function updateData(data: any) {
    if (data) {
        setExitQuestionnaireFormData(data);
    }
}
</script>

<style>
.intro-text {
    text-align: center;
    text-wrap: balance;
    -webkit-text-wrap: balance;
}

.signature {
    display: block;
    text-align: end;
    margin-right: 1rem;
    font-size: var(--fs-300);
    font-weight: 700;
    color: var(--clr-text--muted);
}

.vf-exit-questionnaire-form *,
.vf-exit-questionnaire-form *:before,
.vf-exit-questionnaire-form *:after,
.vf-exit-questionnaire-form:root {
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
