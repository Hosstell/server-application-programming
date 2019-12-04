import { state } from '../store/user'

export default ctx => {
  ctx.store.dispatch('user/getCurrentUser')
}
