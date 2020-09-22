Handling events in Phillip is very, very easy. What is required is 
to inherit base Handler class and override the functions you want to.

---

::: phillip.handlers.Handler

---

All of the functions started with `on_` are event handlers. You only
need to override to work with them. All of the event registration are
all happens in the background--so don't sweat it.

All map events will give you `EventBase` argument, while all user events 
will give you `GroupUser` argument.
