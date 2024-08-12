# shp-yolo-txt

对于一副tiff图，使用Arcmap对目标进行标注得到shapefiles文件

使用该代码可以将tiff图与shapefiles文件作为输入，输出yolo训练的图片，以及对应的标注txt文件。

### 安装必要的库

```
pip install geopandas rasterio shapely numpy opencv-python tqdm
```

### 如何使用？

将**main.py** 中下面的路径进行更改，运行即可。

```
tiff_path = 'path/to/your/tiff.tif'
shapefile_path = 'path/to/your/shapefile.shp'
output_dir = 'path/to/your/output_folder'
pixel_size = 800
```



### 一些解释：

**extend_cut.py**：将shapefile中的每个框向周边扩展至固定尺寸（即pixel_size 大小）然后裁剪输出至output_dir 中，此时output_dir 中包含两个文件夹：

​	shapefiles:将原来的shapefiles扩展至固定大小后生成的shp文件存至此处。

​	tif_folder:对原tiff图按照扩展后的shp文件进行裁剪得到所有的tiff图存至此处。

​		***代码里的输入输出做解释：***

​				在tiff_path 写上tiff图所在位置

​				在shapefile_path 写上shapefile图所在位置

​				在output_dir 写上输出文件夹的位置

​				设置pixel_size 大小



**tif_create_tfw.py**：将tif_folder中的tiff图在指定文件夹下生成对应的tfw文件。

**shp_to_moreshp.py**:将在扩展后的shp文件中每一个框里的所有shapefiles里的小框单独生成一个shp文件至指定文件夹。举例来说对下面的图，shapefiles就是所有的红框，扩展后就变成所有的黄框，这一步就是将每个黄框中的所有红框（不管整个还是半个）生成一个shp文件，所以输出文件夹shp_folder中会有和黄框数量一致的子文件夹，内含各个的shp文件。

![kuang](F:\google_download\picture\kuang.png)

**shp_to_txt.py**：输入shp_folder, tif_folder, tfw_folder,输出txt_folder。旨在将shp文件转化为yolo的txt文件

**txt_kuang.py**：输入tif_folder, txt_folder, 输出verify。旨在将生成的txt文件标注在裁好的图上，用于验证生成的txt是否正确。

> [!WARNING]
>
> 当发现tif_folder里的图片名中的数字大于文件夹中图片总数时，生成的txt会出错。
>
> 经判断应该是最开始的shapefiles文件中中包含未知的框，使得裁图时跳过了部分序号，从而导致后续的txt与裁剪后的图像不匹配。


output_multi	//输出文件夹<br/>
│<br/>
├── shapefiles	//将框扩展到指定大小后生成的shp文件<br/>
│<br/>
├── shp_folder	//大shp中所有的小框生成一个shp<br/>
│<br/>
├── tfw_folder	//扩展后大框对应的tfw<br/>
│<br/>
├── tif_folder	//扩展后的大框<br/>
│<br/>
├── txt_folder	//shp转换的yolo——txt<br/>
│<br/>
└── verify		//将txt绘制在tif上便于验证<br/>
