import bpy
import random

class BlenderRender:
    def __init__(self, bg_path, output_path):
        self.restore_default()
        self.bg_path = bg_path
        self.output_path = output_path

    def add(self):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(random.uniform(-2, 2), random.uniform(-2, 2), random.uniform(-2, 2)), scale=(0.5, 0.5, 0.5))

    def remove_all(self):
        for obj in bpy.data.objects: 
            if obj.name not in ['Camera', 'Light']:
                bpy.data.objects.remove( bpy.data.objects[obj.name], do_unlink=True)

    def get_object_ls(self):
        return [obj.name for obj in bpy.data.objects]

    def restore_default(self):
        return bpy.ops.wm.read_factory_settings()
    
    def render(self, name):
        bpy.context.scene.render.film_transparent = True

        # set node tree
        bpy.data.scenes["Scene"].use_nodes = True
        tree = bpy.context.scene.node_tree
        links = tree.links
        for node in tree.nodes: 
            tree.nodes.remove(node)

        image_node = tree.nodes.new(type='CompositorNodeImage')
        image_node.image = bpy.data.images.load(self.bg_path)
        image_scale_node = tree.nodes.new(type='CompositorNodeScale')
        image_scale_node.space = 'RENDER_SIZE'
        links.new(image_node.outputs[0], image_scale_node.inputs[0])

        render_node = tree.nodes.new(type='CompositorNodeRLayers')
        render_scale_node = tree.nodes.new(type='CompositorNodeScale')
        render_scale_node.space = 'RENDER_SIZE'
        links.new(render_node.outputs[0], render_scale_node.inputs[0])

        alpha_over_node = tree.nodes.new(type='CompositorNodeAlphaOver')
        links.new(image_scale_node.outputs[0], alpha_over_node.inputs[1])
        links.new(render_scale_node.outputs[0], alpha_over_node.inputs[2])

        composite_node = tree.nodes.new(type='CompositorNodeComposite')
        links.new(alpha_over_node.outputs[0], composite_node.inputs[0])

        # render the scene
        bpy.data.scenes["Scene"].render.resolution_x = 1920
        bpy.data.scenes["Scene"].render.resolution_y = 1080
        bpy.data.scenes["Scene"].render.resolution_percentage = 100
        bpy.data.scenes["Scene"].render.filepath = self.output_path+name

        bpy.ops.render.render(write_still=True, use_viewport=True)


def main():
    bg_path = 'background.png'
    output_path = 'img/2/'
    blender_render = BlenderRender(bg_path, output_path)
    blender_render.remove_all()
    for i in range(5):
        blender_render.add()
        blender_render.render(name=f'blender{str(i)}.png')
        blender_render.remove_all()

if __name__ == '__main__':
    main()
