import type { Register } from 'claude-code'

const COMMUNITY_URL = 'https://ai-wizard.tech/'

// Is our banner already in the tree another plugin (or another copy of this one) drew?
const hasBanner = (node: any): boolean =>
  node?.props?.href === COMMUNITY_URL || (node?.children ?? []).some(hasBanner)

export const register: Register = on => {
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) {
      return next(e)
    }

    const below = await next(e)
    if (hasBanner(below)) {
      return below
    }

    const { Box, Link, Text } = $.ui.resolve(e)
    const banner = (
      <Text dimColor>
        🧙 powered by <Link href={COMMUNITY_URL} label="ai-wizard.tech" />
      </Text>
    )

    return below ? <Box flexDirection="column">{below}{banner}</Box> : banner
  })
}
