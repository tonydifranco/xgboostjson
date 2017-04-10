import json
import os
import subprocess
import xgboost as xgb

class XgbJSON:
    nodes = []
    def __init__(self, model_file, fnames=None, na_value='null', regression=False, categoricals=None, base_score=0, sparse_trained=True):
        self.booster = xgb.Booster()
        self.booster.load_model(model_file)
        self.fnames = fnames
        self.na_value = na_value
        self.regression = regression
        self.categoricals = categoricals
        self.base_score = base_score
        self.sparse_trained = sparse_trained

    def to_json(self, fnames=None):
        dump = self.booster.get_dump(with_stats=True, dump_format='json')
        for i, tree in enumerate(dump):
            self.nodes.append([])
            self.recursive_bfs(json.loads(tree))

        for i, n in enumerate(self.nodes):
            self.nodes[i] = """{
                predict: function(d) {
                    return this.n0(d);
                },""" + ','.join(n)


        model_js = """module.exports = {{
            predict: function(d) {{
              return {}this.boosters.map(function(x) {{
                return x.predict(d);
              }}).reduce(function(a, b) {{return a + b;}})){};}},
            boosters: ["""

        if self.regression:
            model_js = model_js.format('Math.exp({} + '.format(base_score), '')
        else:
            model_js = model_js.format('1 / (1 + Math.exp(-', ')')

        model_js = model_js + '},'.join(self.nodes) + '}]};\n'
        with open('tmp.js', 'w') as f:
            f.write(model_js)

        r_uglify_args = ['Rscript', '--vanilla', '-e', 'cat(js::uglify_reformat(readLines("tmp.js"), beautify = TRUE, indent_level = 2))']
        r_uglify = subprocess.run(r_uglify_args, stdout=subprocess.PIPE)

        os.remove('tmp.js')

        return r_uglify.stdout.decode('utf-8')

    def recursive_bfs(self, node):
        self.nodes[-1].append(self.format_node(node))
        if 'children' in node:
            for child in node['children']:
                self.recursive_bfs(child)

    def format_node(self, node):
        if 'leaf' in node:
            inner_js = 'return {leaf};'.format(**node)
        else:
            if self.fnames:
                node['split'] = self.fnames[node['split']]
                stmt = '<'
                val = node['split_condition']
                if self.categoricals:
                    for cat in categoricals:
                        if cat in node['split']:
                            val = node['split'].replace(cat, '')
                            node['split'] = cat
                            stmt = '!=='

            if self.sparse_trained:
                sparse_bool = " || d['{split}'] === 0".format(**node)
            else:
                sparse_bool = ""

            inner_js = """
                if (d['{split}'] === undefined || d['{split}'] === {na_value}{sparse_bool}) {{
                  return this.n{missing}(d);
                }} else if (d['{split}'] {stmt} {val}) {{
                  return this.n{yes}(d);
                }} else {{
                  return this.n{no}(d);
                }}
                """.format(na_value=self.na_value, sparse_bool=sparse_bool, stmt=stmt, val=val, **node)

        node_js = 'n{}: function(d) {{ {} }}\n'.format(node['nodeid'], inner_js)

        return node_js



from sklearn import datasets
import numpy as np
iris = datasets.load_iris()
fnames = [i.replace(' (cm)', '').replace(' ', '_') for i in iris.feature_names]
xgbjson = XgbJSON('python/model.bin', fnames=fnames, na_value='null')

with open('python/model.js', 'w') as f:
    f.write(xgbjson.to_json(fnames=fnames))