import click
import os
from utils import resizeImage, readDir
from moviepy import CompositeVideoClip, ImageClip, VideoFileClip

@click.command()
@click.option('--width', prompt='Width', default=720, help='The width of video clips')
@click.option('--height', prompt='Height', default=1280, help='The height of video clips')
@click.option('--images_origin_dir', prompt='image dir', default='./src/images', help='The source images path')
@click.option('--images_target_dir', prompt='target dir', default='./src/targets', help='The target images path')
@click.option('--music', prompt='Music file', default='./src/music/video.webm', help='The music file')
@click.option('--fps', prompt='video fps ', default=18, help='The output video fps')
@click.option('--output', prompt='Output file', default='./src/dist/1353112775.mp4', help='The output file name')
def main(width, height, images_origin_dir, images_target_dir, music, fps, output):
    if os.path.exists(images_target_dir):
        if not os.path.isdir(images_target_dir):
            raise ValueError(f"{images_target_dir} 已存在但不是目录")
    else:
        os.makedirs(images_target_dir)

    if not os.path.exists(output):
        os.makedirs(output)

    print(f'>>>>>>>>>>>>>>开始处理图片>>>>>>>>>>>>>>')
    origin_images = readDir(images_origin_dir)

    if len(origin_images) == 0:
        print(f"{images_origin_dir} 目录下没有图片")
        return

    print('>>已载入文件 %s 个' % len(origin_images))

    [resizeImage(f, images_target_dir, (width, height)) for f in origin_images]

    target_images = readDir(images_target_dir)

    final_image_clip = None
    # 将高度改成视频的 1/4
    target_resolution = (height/4, None)
    with VideoFileClip(music, target_resolution=target_resolution, has_mask=True) as person_clip:
        print('>>数字人尺寸:(%f, %f)' % (person_clip.w, person_clip.h))
        print('>>数字人视频时长(s):%f' % person_clip.duration)
        image_duration = person_clip.duration / len(target_images) # 每张图片需要播放的时长
        image_clips = []
        for i, f in enumerate(target_images):
            image_clip = (ImageClip(f, duration=image_duration)
                          .with_fps(fps)
                          .with_start(i*image_duration)
                          .with_end((i+1)*image_duration))
            image_clips.append(image_clip)
        final_image_clip = CompositeVideoClip(image_clips)

        # 将person 和 image 堆叠成一个视频
        if final_image_clip is not None:
            with CompositeVideoClip([final_image_clip, person_clip.with_position(('left', 'bottom'))]) as final_video:
                final_video.write_videofile(
                    output,
                    fps=fps,
                    codec='libx264',
                    # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
                    preset='medium',
                    audio_codec="aac",
                    threads=1,
                    bitrate ='2000k')
            print('>>>>>>>>>>>>>>生成视频完成>>>>>>>>>>>>>>')
            print(f'视频地址：{output}')
        else:
            print('>>>>>>>>>>>>>>生成视频失败>>>>>>>>>>>>>>')


if __name__ == '__main__':
    main()
