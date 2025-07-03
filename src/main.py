import click
import os, math
from utils import resizeImage, readDir
from moviepy import TextClip, CompositeVideoClip, AudioFileClip, ImageSequenceClip, ImageClip, VideoFileClip
import moviepy.video.fx as vfx
import librosa

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

    print(f'>>>>>>>>>>>>>>开始处理图片>>>>>>>>>>>>>>')
    origin_images = readDir(images_origin_dir)

    if len(origin_images) == 0:
        print(f"{images_origin_dir} 目录下没有图片")
        return

    print('>>已载入文件 %s 个' % len(origin_images))
    print(origin_images)

    for f in origin_images:
        resizeImage(f, images_target_dir, (width, height))

    target_images = readDir(images_target_dir)

    target_resolution = (height/4, None)
    person_clip = VideoFileClip(music, target_resolution=target_resolution, has_mask=True)
    print('>>数字人尺寸:(%f, %f)' % (person_clip.w, person_clip.h))
    # (ih, iw) = (person_clip.h, person_clip.w)
    # scale_size = min(width / iw, height / ih)
    # new_size = (int(iw * scale_size), int(ih * scale_size))
    # person_clip.target_resolution = new_size
    # 获取视频的时长，将图片平均分配到这些时长中
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
    final_video = CompositeVideoClip([final_image_clip, person_clip.with_position(('left', 'bottom'))])

    # y, sr = librosa.load(music, sr=None)
    # tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    # beat_times = list(librosa.frames_to_time(beats, sr=sr))
    # beat_times.append(beat_times[-1] + 1)
    #
    # clips = []
    # audio_time = librosa.get_duration(filename=music)
    # print('>>音频时长(s):%f >>节拍数量：%s' % (audio_time, len(beat_times)))
    # '''
    # 计算节拍数量和相片数量的差值比例，以计算需要在每幅相片后补足多少帧，
    # 这里计算的差值，是为了让相片能补足节拍的数量，多跨几个节拍，让每一幅相片停留更长时间。
    # '''
    # interval = math.ceil(len(beat_times) / len(target_images))
    # filesPath = []
    # for f in target_images:
    #     filesPath.extend([f] * interval)
    #
    # print('>>新的文件列表长度:%s' % len(filesPath))
    # print('>>>>>>>>>>>>>>开始按节拍生成视频帧>>>>>>>>>>>>>>')
    #
    # for index, beat_time in enumerate(beat_times[:-1]):
    #     if index >= len( filesPath):
    #         print('>>图片数量不足以匹配节拍，中止匹配。输出的视频后段可能会出现黑屏。')
    #         print('>>图片数量：{0} >节拍数量：{1}'.format(len( filesPath), len(beat_times)))
    #         break
    #     print(f'{index + 1}/{len(beat_times)}>>{ filesPath[index]}')
    #     time_diff = math.modf(beat_time - beat_times[index -1])
    #     time_diff = math.ceil(time_diff[0]*10) if (time_diff[0] * 10) > time_diff[-1] else math.ceil(time_diff[-1])
    #     image_clip = ((ImageClip(filesPath[index], duration=abs(time_diff)*fps)
    #                   .with_fps(abs(time_diff)*fps))
    #                   .with_start(beat_time)
    #                   .with_end(beat_times[index + 1]))
    #     image_clip = image_clip.with_position('center')
    #     # if index != 0 and index % interval == 0:
    #     #     image_clip = vfx.FadeIn(image_clip)
    #     clips.append(image_clip)
    #
    #
    # print('>>>>>>>>>>>>>>开始合并剪辑，生成视频>>>>>>>>>>>>>>')
    # final_clip = CompositeVideoClip(clips)
    # audio_clip = AudioFileClip(music)
    # final_video = final_clip.with_audio(audio_clip)
    final_video.write_videofile(
        output,
        fps=fps,
        codec='libx264',
        # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo
        preset='veryfast',
        audio_codec="aac",
        threads=8,
        bitrate ='2000k')
    final_video.close()
    print('>>>>>>>>>>>>>>生成视频完成>>>>>>>>>>>>>>')
    print(f'视频地址：{output}')

if __name__ == '__main__':
    main()