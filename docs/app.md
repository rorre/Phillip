Phillip is running on top of its instance which controls all the workflow
and the way of the app behaves.

---

::: phillip.application.Phillip

---

### Running

To run, you only need to supply `token`, and either of `webhook_url` or `handlers`.
If both could not be found, it will raise an `Exception` as they're needed in order to run.

```python
from phillip.application import Phillip
p = Phillip(
    "0c38a********************", # osu! API token
    webhook_url="https://discordapp.com/api/webhooks/************" # Discord webhook URL
)
p.run()
```

### Configuration

* You may have a checkpoint of nomination feed by setting a kwarg value og `last_date` to your desired date.
* You could disable groupfeed or mapfeed functionality by disabling them upon init.

!!! warning
    You should always disable the functionality when it is not needed, as it will cost you
    internet fees and unnecessary rate limiting.

!!! tip
    If you want to add another handler after the app started, you could use the
    `add_handler(handler)` function.
