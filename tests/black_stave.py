from neoscore.common import *

neoscore.setup()

save_path = "../OshunAI/media/empty_staves/"

empty_staff = Staff(ORIGIN, None, Mm(200), line_spacing=Mm(5))

Clef(Mm(60), empty_staff, 'treble')

save_dest = save_path + "empty_treble.png"

neoscore.render_image(rect=None,
                      dest=save_dest,
                      autocrop=True,
                      preserve_alpha=False,
                      wait=True
                      )
