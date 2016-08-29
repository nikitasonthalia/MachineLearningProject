import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import org.apache.spark.storage.StorageLevel
object Cooccurrence {
  def main(args: Array[String]){
  val sc = new SparkContext(new SparkConf().setAppName("matrix")
    .setMaster("local[7]") 
     .set("spark.executor.memory", "4g")
     .set("spark.driver.memory","5g"));
    for( a <- 3 to 10){
       
    val textFile = sc.textFile("MLprojectOutput/train_week"+a+".csv")
    val pro = textFile.map(line => {
    val token = line.split(",");
    val key = token(4);
    // For product matrix
    val valueP = token(5) +"#"+ token(10);
    (key,valueP)}).groupByKey;

    val dep= textFile.map(line => {
    val token = line.split(",");
    val key = token(4);
     //For depot matrix
    val valueD = token(1) +"#"+ token(10);
    (key,valueD)}).groupByKey;

    pro.coalesce(1).saveAsObjectFile("MLprojectOutput/week"+a+"Pobjectoutput")
    dep.coalesce(1).saveAsObjectFile("MLprojectOutput/week"+a+"Dobjectoutput")

    val valuefileP =  sc.objectFile[(Char, Seq[(String)])]("MLprojectOutput/week"+a+"Pobjectoutput/part-00000");
    val valuefileD =  sc.objectFile[(Char, Seq[(String)])]("MLprojectOutput/week"+a+"Dobjectoutput/part-00000");
    val outputP= valuefileP.persist(StorageLevel.MEMORY_AND_DISK_SER).flatMap( {
      case (userid, values) =>
      {
        var productIds = values.map(value=>value.split("#")(0));
        var demand = values.map(value=>value.split("#")(1));
        productIds.combinations(2).map(
          pairs => {
             {(pairs.mkString("#"), 1)}
          })
    }}).reduceByKey(_ + _);

    val outputD= valuefileD.persist(StorageLevel.MEMORY_AND_DISK_SER).flatMap( {
      case (userid, values) =>
      {
        var productIds = values.map(value=>value.split("#")(0));
        var demand = values.map(value=>value.split("#")(1));
        productIds.combinations(2).map(
          pairs => {
             {(pairs.mkString("#"), 1)}
          })
    }}).reduceByKey(_ + _);

  outputP.coalesce(1).saveAsTextFile("MLprojectOutput/week"+a+"ProductMatrix")
  outputD.coalesce(1).saveAsTextFile("MLprojectOutput/week"+a+"DepotMatrix")
 }
}
  }
