# 准备环境
- 项目使用poetry进行管理，在开始之前，先安装[poetry](https://blog.kyomind.tw/python-poetry/)
- 项目使用python版本为>3.13，事实上3.9以上都可以，如果需要更改版本，需要修改pyproject.toml中的依赖
- 确保你安装了指定的python版本

## 初始化poetry环境
当通过git clone下来完整的项目后，首先需要初始化虚拟环境，执行如下命令：
```commandline
poetry config virtualenvs.in-project true
poetry env remove python
```
poetry config 执行后会将.venv安装到当前工程目录下，如果不执行，会安装到Poetry Cache里

## 启动环境
```commandline
source .venv/bin/activate
```
如果需要退出，直接执行 deactivate 即可

## 使用poetry 安装套件
```commandline
poetry add xxx
```

因为我们会使用 opencv-python 依赖，可以尝试安装此依赖：
```commandline
poetry add opencv-python
```
安装之后，查看 pyproject.toml 中，增加了依赖，并将此包安装到了虚拟环境中，后续可以通过此命令安装所需的包
> opencv-python (>=4.11.0.86,<5.0.0.0)

如果要移除某一个套件，可以使用如下命令：
```commandline
poetry remove xxx
```

## 安装所有依赖
我们已经把项目所需的所有依赖都放到了 pyproject.toml 中，在正式执行之前，需要先安装所有依赖，执行如下命令：
```commandline
poetry install
```

然后安装必要的依赖
```commandline
pip install opencv-python Pillow click librosa
```

以下是moviepy源码需要的依赖
```commandline
pip install proglog imageio
```

# MoviePy

MoviePy (online documentation [here](https://zulko.github.io/moviepy/)) is a Python library for video editing: cuts, concatenations, title insertions, video compositing (a.k.a. non-linear editing), video processing, and creation of custom effects.

MoviePy can read and write all the most common audio and video formats, including GIF, and runs on Windows/Mac/Linux, with Python 3.9+.

# Example

In this example we open a video file, select the subclip between 10 and
20 seconds, add a title at the center of the screen, and write the
result to a new file:

``` python
from moviepy import VideoFileClip, TextClip, CompositeVideoClip

# Load file example.mp4 and keep only the subclip from 00:00:10 to 00:00:20
# Reduce the audio volume to 80% of its original volume

clip = (
    VideoFileClip("long_examples/example2.mp4")
    .subclipped(10, 20)
    .with_volume_scaled(0.8)
)

# Generate a text clip. You can customize the font, color, etc.
txt_clip = TextClip(
    font="Arial.ttf",
    text="Hello there!",
    font_size=70,
    color='white'
).with_duration(10).with_position('center')

# Overlay the text clip on the first video clip
final_video = CompositeVideoClip([clip, txt_clip])
final_video.write_videofile("result.mp4")
```

# How MoviePy works

Under the hood, MoviePy imports media (video frames, images, sounds) and converts them into Python objects (numpy arrays) so that every pixel becomes accessible, and video or audio effects can be defined in just a few lines of code (see the [built-in effects]() for examples).

The library also provides ways to mix clips together (concatenations, playing clips side by side or on top of each other with transparency, etc.). The final clip is then encoded back into mp4/webm/gif/etc.

This makes MoviePy very flexible and approachable, albeit slower than using ffmpeg directly due to heavier data import/export operations.