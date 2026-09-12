# VSC Public Plugin Submission

## Listing

- Display name: VSC 创作入口
- Developer: VibeShotClub
- Category: Productivity
- Website: https://vibeshot.club
- Support: https://vibeshot.club/support
- Privacy: https://vibeshot.club/privacy
- Terms: https://vibeshot.club/terms
- Version: 0.1.0
- Release notes: Initial public VSC skills-only plugin package with unified routing for image and video creative workflows.

## Starter prompts

1. `@vsc创作入口，生成一张风雨交加街头的真实人像照片。`
2. `$vsc 给这个人物做一张自然生活感抓拍照片。`
3. `@vsc创作入口，给这个主体探索 8 种稀有视觉风格，只要提示词。`

## Positive test cases

1. With an uploaded adult portrait, `@vsc创作入口 @创建图片，风雨交加的街头！` should enter the VSC router first, preserve the uploaded identity reference, select the best matching portrait workflow, and only then bridge to native image generation when available.
2. `$vsc 给陶瓷猫香水瓶探索 8 种稀有视觉风格，只要提示词。` should route to rare-style-explorer and return prompts only.
3. `$vsc 九尾狐衔灯走过雪夜竹林，工笔水墨奇幻。` should route to shan-ze-school.
4. `$vsc 两位成年朋友在泳池泼水，朋友视角，一张照片。` should route to summer-boyfriend-pov and keep the single-image scope.
5. `$vsc 制作一对成年情侣在巴塞罗那旅行的虚拟 Vlog 方案。` should route to virtual-couple-travel-vlog and respect the requested workflow scope.

## Negative test cases

1. `帮我写一封请假邮件。` should not invoke VSC.
2. `总结这份财务表格。` should not invoke VSC.
3. `@vsc创作入口` with no creative task context should present a short capability guide and ask what the user wants to create, without starting image or video generation.

## Publication gates

- Repository plugin validation must pass.
- Public submission account must have Apps Management: Write for the target OpenAI Platform organization.
- Developer or business identity must be verified before public submission.
- Upload the skills-only plugin bundle and listing assets in the OpenAI plugin submission portal.
- After approval, publish to the universal Plugins Directory and verify invocation from ChatGPT and Codex surfaces supported for the account.
