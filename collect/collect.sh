
rm -rf png*

mkdir png_prior
mkdir png_post

find ../ -type d -wholename "*/Output/png_prior" -exec sh -c 'cp "$1"/*.png ./png_prior' sh {} \;
find ../ -type d -wholename "*/Output/png_post" -exec sh -c 'cp "$1"/*.png ./png_post' sh {} \;