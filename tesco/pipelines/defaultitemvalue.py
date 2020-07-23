from tesco.items import ProductItem


class DefaultItemValuePipeline:

    def process_item(self, item, spider):
        if isinstance(item, ProductItem):
            item.setdefault('price', None)
            item.setdefault('description', None)
            item.setdefault('name_and_address', None)
            item.setdefault('return_address', None)
            item.setdefault('net_contents', None)
        return item
