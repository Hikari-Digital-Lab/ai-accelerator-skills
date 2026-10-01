import { test, expect } from 'claude-code/testing'

test('shows powered by line', async $ => {
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ plugin: 'skills-basic', surface, component: 'AbovePrompt', props: { hasSurvey: false } })
    expect(await ui.find({ type: 'Text', text: /powered by/ })).toBeDefined()
    await ui.unmount()
  }
})
