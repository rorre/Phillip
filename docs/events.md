The event object fired to the event handlers could be splitted into two, `EventBase` or `GroupUser`.

### EventBase

`EventBase` is used for map events, they have their own classes for each event which always inherits from this class.
The only diffrrence is that they're using different mechanism to gather info and maybe additional info (such as source post for bubble pops).

::: phillip.abc.EventBase
    :docstring:
    :members:

### GroupUser

`GroupUser` rrepresents a user inside a group that is defined from scraping the site.

::: phillip.osu.classes.web.GroupUser
    :docstring:

!!! warning
    This class may change in the future as osu!web development goes.
