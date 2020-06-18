from talon import Context, actions

ctx = Context()


@ctx.action_class("core")
class Actions:
    def run_talon_script(ctx, script, m):
        with ctx:
            print(ctx)
            print(script)
            print(m)
            script.run(actions, namespace=m)
