# obsidian

Obsidian is a constraint-based system for generating technical diagrams
([though you can draw other things with it, too](https://github.com/wootfish/obsidian/blob/master/examples/gallery/go_board.png)).
It lets you write terse, descriptive scripts which produce publication-quality
vector or raster graphics.

The design and API are partly inspired by [this blog post](https://www.anishathalye.com/2019/12/12/constraint-based-graphic-design/)
on an interesting (but unfortunately closed-source, and possibly abandoned)
constraint-based graphic design tool.

# setup

Obsidian currently only targets Python 3.7. This is because it depends on
`dataclasses` (which were added to stdlib in 3.7) and `pysmt` (which may have
issues on 3.8 or later).

You will also need Cairo. Depending on your platform this can be installed with
`sudo apt install libcairo2`, `brew install cairo`, or similar.

Obsidian is still under heavy development, so I haven't put it on PyPI yet.

Dev setup instructions:

```
$ git clone git@github.com:wootfish/obsidian.git
$ cd obsidian
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -e .
(venv) $ pysmt-install --z3
```

If all goes well, then (with your virtualenv active) you should be able to `cd`
into the `examples` folder, run any of the scripts there, and see no errors
(aside from the deprecation warning thrown by `pysmt`).

# usage notes

The basic idea is to create some `Shape`s, put them into a `Group`, specify
their juxtaposition through a list of constraints passed to that `Group`, and to
render the `Group` using a `Canvas`.

`Group`s may be placed within other `Group`s without surprises or complications,
permitting a modular design pattern where different regions of a diagram can be
specified independently and then composed.

Explicit coordinates do not often get specified in Obsidian; in fact, for most
images they are not necessary _at all_. However, just so you know: We place the
origin in the top-left, with +x pointing right and +y pointing down.

(This is the convention used by most graphics editing tools; however, it is in
open defiance of our graphics library, which places the origin in the bottom
left with +y pointing up; I know that's how people draw x-y axes on paper and
also how GL does things, but god dammit it just ain't right.)

Until we write some proper docs, the best usage guide is the `examples` folder.
I've done my best to keep the examples terse and clear. If you have any
questions, you can reach me [on Twitter](https://twitter.com/elisohl) or
[elsewhere](https://eli.sohl.com/contact).
