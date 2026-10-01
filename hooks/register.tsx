import type { Register } from 'claude-code'

const COMMUNITY_URL = 'https://ai-wizard.tech/'

export const register: Register = on => {
  on('ui.render', { component: 'AbovePrompt' }, ($, e, next) => {
    if (e.props.hasSurvey) {
      return next(e)
    }

    const { Link, Text } = $.ui.resolve(e)

    return (
      <Text dimColor>
        🧙 powered by <Link href={COMMUNITY_URL} label="ai-wizard.tech" />
      </Text>
    )
  })
}
